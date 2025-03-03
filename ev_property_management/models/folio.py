# -*- coding: utf-8 -*-

from odoo import _, api, models, fields


class UnitFolio(models.Model):
    _name = "unit.folio"
    _description = 'Folio'
    _order = 'name, id'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

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
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        default=_default_currency_id,
        required=True,
        tracking=1,
    )
    reservation_id = fields.Many2one('unit.reservation', string="Reservation" ,required=True, readonly="1")
    partner_id = fields.Many2one(related='reservation_id.partner_id')
    partner_phone = fields.Char(related='partner_id.phone')
    partner_email = fields.Char(related='partner_id.email')
    check_in_date = fields.Datetime(string="Check-In Date", required=True, copy=False)
    check_out_date = fields.Datetime(string="Check-Out Date", required=True, copy=False)
    state = fields.Selection(
        [('checked_in', 'Checked-In'),('in_progress', 'In Progres'), ('checked_out', 'Checked-Out'), ('cancel', 'Cancel'),
         ('done', 'Done')],
        default="checked_in", tracking=True)
    room_line_ids = fields.One2many('folio.room.line', 'folio_id', "Room Details")
    guest_line_ids = fields.One2many('folio.guest.line', 'parent_id', 'Guest Details')
    service_line_ids = fields.One2many('folio.service.line', 'parent_id', 'Additional Services')
    pos_order_line_ids = fields.One2many('pos.order', 'folio_id', 'Guest Details')
    no_of_adults = fields.Integer('No Of Adults')
    no_of_children = fields.Integer('No Of Children')
    folio_total = fields.Monetary('Total', compute="_compute_reservation_total")
    folio_subtotal = fields.Monetary('Untaxed Amount)', compute="_compute_reservation_total")
    folio_tax_price = fields.Monetary('Taxes)', compute="_compute_reservation_total")

    price_list_id = fields.Many2one(comodel_name='product.pricelist',
                                    string="PriceList",
                                    compute='_compute_partner_pricelist',
                                    store=True, readonly=False,
                                    required=True,
                                    tracking=1, )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('unit.folio') or 'New'
        return super(UnitFolio, self).create(vals)

    def button_confirm(self):
        for rec in self:
            rec.write({'state': 'in_progress'})

    def button_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})

    def button_done(self):
        for rec in self:
            rec.write({'state': 'done'})

    def button_checked_out(self):
        for rec in self:
            rec.write({'state': 'checked_out'})

    def button_set_to_draft(self):
        for rec in self:
            rec.write({'state': 'checked_in'})



class FolioRoomLines(models.Model):
    _name = 'folio.room.line'
    _description = "Folio Lines"
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

    folio_id = fields.Many2one('unit.folio')
    unit_type_id = fields.Many2one('unit.type', string='Unit Type')
    quantity = fields.Integer('No of Rooms', default=1, readonly=True)
    unit_id = fields.Many2one('property.unit')
    currency_id = fields.Many2one(related='folio_id.currency_id')
    price_unit = fields.Float(related='unit_id.price', store=True)
    tax_ids = fields.Many2many('account.tax', 'unit_folio_line_taxes_rel', 'folio_id', 'tax_id',
                               string="Taxes",
                               help="Default taxes used when selling the Unit",
                               domain=[('type_tax_use', '=', 'sale')],
                               default=lambda
                                   self: self.env.companies.account_sale_tax_id or self.env.companies.root_id.sudo().account_sale_tax_id,
                               )
    check_in_date = fields.Datetime(related='folio_id.check_in_date')
    check_out_date = fields.Datetime(related='folio_id.check_out_date')
    uom_qty = fields.Float('No Of Days', compute="_compute_no_of_days")
    price_sub_total = fields.Monetary('Subtotal', compute="_compute_price_total")
    price_total = fields.Monetary('Total', compute="_compute_price_total")
    price_tax = fields.Monetary('Tax', compute="_compute_price_total")


class FolioGuestLines(models.Model):
    _name = 'folio.guest.line'
    _description = "Guest Details"
    _order = "id"

    parent_id = fields.Many2one('unit.folio')
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


class FolioServiceLines(models.Model):
    _name = 'folio.service.line'
    _description = "Services"
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
                'partner_id': self.parent_id.partner_id,
                'currency_id': self.currency_id,
            },
        )

    @api.depends('uom_qty', 'price_unit', 'tax_ids')
    def _compute_price_total(self):
        """Compute the amounts for reservation line."""
        for line in self:
            base_line = line._prepare_base_line_for_taxes_computation()
            self.env['account.tax']._add_tax_details_in_base_line(base_line, self.env.company)
            line.price_sub_total = base_line['tax_details']['raw_total_excluded_currency']
            line.price_total = base_line['tax_details']['raw_total_included_currency']
            line.price_tax = line.price_total - line.price_sub_total

    parent_id = fields.Many2one('unit.folio')
    product_id = fields.Many2one('product.template', string="Product",
                                 domain=[('sale_ok', '=', True), ('type', '=', 'service')])
    name = fields.Char('Description')
    uom_qty = fields.Integer('Quantity')
    price_unit = fields.Float(string='Price', store=True)
    tax_ids = fields.Many2many('account.tax', 'folio_service_line_taxes_rel', 'folio_id', 'tax_id',
                               string="Taxes",
                               domain=[('type_tax_use', '=', 'sale')],
                               default=lambda
                                   self: self.env.companies.account_sale_tax_id or self.env.companies.root_id.sudo().account_sale_tax_id,
                               )
    price_sub_total = fields.Monetary('Subtotal', compute="_compute_price_total")
    price_total = fields.Monetary('Total', compute="_compute_price_total")
    price_tax = fields.Monetary('Tax', compute="_compute_price_total")
    currency_id = fields.Many2one(related='parent_id.currency_id')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        for rec in self:
            unit_price = False
            tax_ids = []
            if rec.product_id:
                unit_price = rec.product_id.list_price
                tax_ids = rec.product_id.taxes_id
            rec.write({
                'price_unit' : unit_price,
                'tax_ids' : [(6, 0, tax_ids.ids)] if tax_ids else False
            })


class PosOrder(models.Model):
    _name = "pos.order"
    _inherit = ["pos.order"]

    folio_id = fields.Many2one('unit.folio')
