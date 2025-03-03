# -*- coding: utf-8 -*-

from odoo import models, fields


class PropertyUnit(models.Model):
    """Model that holds all details regarding a property unit."""
    _name = "property.unit"
    _description = "Property Units"
    _order = "unit_id, id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", index="trigram", required=True, translate=True)
    unit_id = fields.Char("Unit ID", required=True, copy=False, default="New", index="trigram")
    property_id = fields.Many2one("property.master", string="Property", required=True)

    # Related fields (Add store=True if you need to filter/sort/search)
    pp_type = fields.Selection(related="property_id.pp_type", store=True)
    pp_sub_type_id = fields.Many2one(related="property_id.pp_sub_type_id", store=True)

    unit_type = fields.Many2one("unit.type", string="Type", required=True)
    image = fields.Image(string="Image", max_width=1920, max_height=1920)
    area = fields.Float(related='unit_type.area')
    furnishing_status = fields.Selection(
        [("furnished", "Furnished"), ("semi_furnished", "Semi-Furnished"), ("unfurnished", "Unfurnished")],
        default="furnished",
        string="Furnishing Status",
    )

    status = fields.Selection(
        [("vacant", "Vacant"), ("occupied", "Occupied"), ("reserved", "Reserved"),
         ("under_maintenance", "Under Maintenance")],
        default="vacant",
        string="Status",tracking=True
    )

    description = fields.Text(related='unit_type.description')
    policy = fields.Text(related='unit_type.policy')
    taxes_ids = fields.Many2many(related='unit_type.taxes_ids')
    services_ids = fields.Many2many(related='unit_type.services_ids')
    facility_ids = fields.Many2many(related='unit_type.facility_ids')
    smoking_allowed = fields.Boolean(string="Smoking Allowed", default=False)
    parking_available = fields.Boolean(string="Parking Available", default=True)
    max_adults = fields.Integer(related='unit_type.max_adults')
    max_children = fields.Integer(related='unit_type.max_children')
    product_id = fields.Many2one(related='unit_type.product_id')
    price = fields.Float(related='unit_type.price', store=True)
    next_available_date = fields.Datetime('Next Available date', readonly=1)


class UnitType(models.Model):
    """Model holding details regarding unit types."""
    _name = "unit.type"
    _description = "Unit Types"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Name", index="trigram", required=True, translate=True)
    pp_sub_type_id = fields.Many2one("property.sub.type", string="Property Sub Category")
    description = fields.Text(string="Description", translate=True)
    policy = fields.Text(string="Policy", translate=True)
    area = fields.Float(string='Area(sqm)')
    price = fields.Float('Price')
    taxes_ids = fields.Many2many('account.tax', 'unit_type_taxes_rel', 'unit_type_id', 'tax_id',
                                string="Taxes",
                                help="Default taxes used when selling the Unit Type",
                                domain=[('type_tax_use', '=', 'sale')],
                                default=lambda
                                    self: self.env.companies.account_sale_tax_id or self.env.companies.root_id.sudo().account_sale_tax_id,
                                )

    services_ids = fields.Many2many('unit.service', 'unit_service_type_rel', 'service_id', 'type_id', string="Services")
    facility_ids = fields.Many2many('unit.facility', 'unit_facility_type_rel', 'facility_id', 'type_id', string="Facilities")
    smoking_allowed = fields.Boolean(string="Smoking Allowed", default=False)
    parking_available = fields.Boolean(string="Parking Available", default=True)

    max_adults = fields.Integer(string="Max Adults")
    max_children = fields.Integer(string="Max Children")
    product_id = fields.Many2one("product.template", string="Related Product")


class UnitService(models.Model):
    """Model holding details regarding unit services."""
    _name = "unit.service"
    _description = "Services"

    name = fields.Char(string="Name", index="trigram", required=True, translate=True)
    icon = fields.Image(string="Icon")


class UnitFacility(models.Model):
    """Model holding details regarding unit facilities."""
    _name = "unit.facility"
    _description = "Facilities"

    name = fields.Char(string="Name", index="trigram", required=True, translate=True)
    icon = fields.Image(string="Icon")

