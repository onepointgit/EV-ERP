# -*- coding: utf-8 -*-

from odoo import models, fields, _

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    print_product_default_code_receipt = fields.Boolean(string=_("Product internal reference on receipt"), default=True)