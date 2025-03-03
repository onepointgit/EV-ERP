# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PropertyMaster(models.Model):
    """Model that holds all details regarding property"""
    _name = 'property.master'
    _description = 'Properties'
    _order = 'pp_id,id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', help="Property Name", index='trigram',
                required=True, translate=True)
    pp_id = fields.Char('Property ID', required=True, index='trigram', copy=False, default='New')
    pp_type = fields.Selection([('residential', 'Residential'), ('commercial', 'Commercial')], default="residential", string='Type')
    pp_sub_type_id = fields.Many2one('property.sub.type', string="Sub Category", required=True, copy=False)
    pp_image = fields.Image(string="Image", max_width=1920,
                              max_height=1920, help='Image of the property')
    #<address>
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip')
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
    # </address>
    area = fields.Float(string='Area(sqm)')
    status = fields.Selection([('active', 'Active'), ('under_maintenance', 'Under Maintenance'), ('closed', 'Closed'),
                               ('leased', 'Leased')], default="active", string='Status', tracking=True)
    description = fields.Html(string='Property Description', help="Add description",
                              translate=True)
    unit_ids = fields.One2many('property.unit', 'property_id',"Units",copy=False)





