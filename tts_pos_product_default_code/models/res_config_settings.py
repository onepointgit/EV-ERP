# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    pos_print_product_default_code_receipt = fields.Boolean(related='pos_config_id.print_product_default_code_receipt', readonly=False)