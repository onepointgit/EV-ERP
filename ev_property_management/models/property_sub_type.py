# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PropertyMaster(models.Model):
    """Model that holds all details regarding property"""
    _name = 'property.sub.type'
    _description = 'Properties'

    name = fields.Char(string='Name', help="Property Name", index='trigram',
                required=True, translate=True)
    pp_type = fields.Selection([('residential', 'Residential'), ('commercial', 'Commercial')], default="residential", string='Type')
    type = fields.Selection([('hotel', 'Hotel'),('villa', 'Villa'),('others', 'Others')], string='Type')





