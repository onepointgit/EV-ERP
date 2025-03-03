# -*- coding: utf-8 -*-

from odoo import _, api, models, fields
from odoo.exceptions import UserError


class UnitReservation(models.Model):
    _name = "unit.reservation"
    _description = "Reservations"
    _order = "name, id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.depends('reservation_line_ids')
    def _compute_reservation_total(self):
        total = 0
        untaxed = 0
        tax_amt = 0
        for rec in self:
            for line in rec.reservation_line_ids:
                total += line.price_total
                untaxed += line.price_sub_total
                tax_amt += line.price_tax
            rec.reservation_total = total
            rec.reservation_subtotal = untaxed
            rec.reservation_tax_price = tax_amt

    @api.depends('partner_id')
    def _compute_partner_pricelist(self):
        """Computes  partner PriceList"""
        for rec in self:
            if not rec.partner_id:
                rec.price_list_id = False
                continue
            rec = rec.with_company(rec.company_id)
            rec.price_list_id = rec.partner_id.property_product_pricelist

    name = fields.Char('Order Reference', required=True, index='trigram', copy=False, default='New')
    date = fields.Date(help='Reservation Date', string='Date', default=fields.Date.context_today)
    pp_sub_type_id = fields.Many2one('property.sub.type', string="Sub Category", required=True, copy=False)
    source_id = fields.Many2one('source.master', string='Source')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=_default_currency_id,
        required=True,
        tracking=1,
    )
    price_list_id = fields.Many2one(comodel_name='product.pricelist',
                                    string="PriceList",
                                    compute='_compute_partner_pricelist',
                                    store=True, readonly=False,
                                    required=True,
                                    tracking=1, )
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, copy=False)
    partner_phone = fields.Char(related='partner_id.phone')
    partner_email = fields.Char(related='partner_id.email')
    check_in_date = fields.Datetime(string="Check-In Date", required=True, copy=False)
    check_out_date = fields.Datetime(string="Check-Out Date", required=True, copy=False)
    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('checked_in', 'Checked-In'), ('checked_out', 'Checked-Out'),
         ('done', 'Done'), ('cancel', 'Cancelled')],
        default="draft", tracking=True)
    reservation_line_ids = fields.One2many('unit.reservation.line', 'reservation_line_id', "Reservation Details")
    guest_line_ids = fields.One2many('reservation.guest.line', 'parent_id', 'Guest Details')
    no_of_adults = fields.Integer('No Of Adults')
    no_of_children = fields.Integer('No Of Children')
    reservation_total = fields.Monetary('Total', compute="_compute_reservation_total")
    reservation_subtotal = fields.Monetary('Untaxed Amount)', compute="_compute_reservation_total")
    reservation_tax_price = fields.Monetary('Taxes)', compute="_compute_reservation_total")
    company_id = fields.Many2one('res.company', string="Company",
                                 required=True, index=True,
                                 default=lambda self: self.env.company)
    folio_ids = fields.One2many('unit.folio', 'reservation_id', string="Folio")

    def button_confirm(self):
        for rec in self:
            rec.write({'state': 'confirmed'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})

    def button_set_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    def button_checked_in(self):
        for rec in self:
            rec.button_generate_folio()
            rec.write({'state': 'done'})

    def button_generate_folio(self):
        folio_obj = self.env['unit.folio'].sudo()
        for rec in self:
            folio = folio_obj.create({
                'currency_id': rec.currency_id.id,
                'partner_id': rec.partner_id.id,
                'reservation_id': rec.id,
            })

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("reservation.ref") or "New"
        return super(UnitReservation, self).create(vals)


class UnitReservationLines(models.Model):
    _name = 'unit.reservation.line'
    _description = "Reservations Details"
    _order = "id"

    def _prepare_base_line_for_taxes_computation(self):
        """ Convert the current record to a dictionary in order to use the generic taxes computation method
        defined on account.tax.

        :return: A python dictionary.
        """
        self.ensure_one()
        return self.env['account.tax']._prepare_base_line_for_taxes_computation(
            self,
            **{
                'tax_ids': self.tax_ids,
                'quantity': self.uom_qty,
                'partner_id': self.reservation_line_id.partner_id,
                'currency_id': self.currency_id,
            },
        )

    @api.depends('check_in_date', 'check_out_date')
    def _compute_no_of_days(self):
        for rec in self:
            no_of_days = 0
            if rec.check_in_date and rec.check_out_date:
                no_of_days = (rec.check_out_date - rec.check_in_date).days
            rec.uom_qty = no_of_days

    @api.depends('no_of_days', 'price')
    def _compute_reservation_subtotal(self):
        total_price = self.no_of_days * self.price
        self.sub_total = total_price

    @api.depends('uom_qty', 'price_unit', 'tax_ids')
    def _compute_price_total(self):
        """Compute the amounts for reservation line."""
        for line in self:
            base_line = line._prepare_base_line_for_taxes_computation()
            self.env['account.tax']._add_tax_details_in_base_line(base_line, self.env.company)
            line.price_sub_total = base_line['tax_details']['raw_total_excluded_currency']
            line.price_total = base_line['tax_details']['raw_total_included_currency']
            line.price_tax = line.price_total - line.price_sub_total

    # def _domain_unit_type(self):
    #     for rec in self:
    #         pp_sub_type = rec.reservation_line_id.pp_sub_type_id
    #         unit_types = rec.env['unit.type'].search([('pp_sub_type_id', '=', pp_sub_type.id)])
    #         domain = [('id', 'in', unit_types.ids)]
    #         return domain

    reservation_line_id = fields.Many2one('unit.reservation')
    unit_type_id = fields.Many2one('unit.type', string='Unit Type')
    quantity = fields.Integer('No of Rooms', default=1, readonly=True)
    unit_id = fields.Many2one('property.unit')
    currency_id = fields.Many2one(related='reservation_line_id.currency_id')
    price_unit = fields.Float(related='unit_id.price', store=True)
    tax_ids = fields.Many2many('account.tax', 'unit_reserv_line_taxes_rel', 'reserve_line_id', 'tax_id',
                               string="Taxes",
                               help="Default taxes used when selling the Unit",
                               domain=[('type_tax_use', '=', 'sale')],
                               default=lambda
                                   self: self.env.companies.account_sale_tax_id or self.env.companies.root_id.sudo().account_sale_tax_id,
                               )
    check_in_date = fields.Datetime(related='reservation_line_id.check_in_date')
    check_out_date = fields.Datetime(related='reservation_line_id.check_out_date')
    uom_qty = fields.Float('No Of Days', compute="_compute_no_of_days")
    price_sub_total = fields.Monetary('Subtotal', compute="_compute_price_total")
    price_total = fields.Monetary('Total', compute="_compute_price_total")
    price_tax = fields.Monetary('Tax', compute="_compute_price_total")


class ReservationGuestLines(models.Model):
    _name = 'reservation.guest.line'
    _description = "Guest Details"
    _order = "id"

    parent_id = fields.Many2one('unit.reservation')
    unit_id = fields.Many2one('property.unit')
    document_id = fields.Char(string="Document ID", required=True, copy=False, index=True)
    document_type_id = fields.Many2one('document.type', string="Document Type", required=True)
    valid_from = fields.Date(string="Valid From", required=True)
    valid_to = fields.Date(string="Valid To", required=True)
    guest_name = fields.Char(string="Guest Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender", required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    country = fields.Many2one('res.country', string="Country", required=True)


class DocumentType(models.Model):
    _name = "document.type"
    _description = "Document Type"

    name = fields.Char(string="Document Type", required=True, unique=True)
    description = fields.Text(string="Description")


class SourceMaster(models.Model):
    _name = 'source.master'
    _description = "Source master"
    _order = "id"

    name = fields.Char('Source', copy=False)
