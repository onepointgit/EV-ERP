# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    multi_receipt_count = fields.Integer(related='pos_config_id.multi_receipt_count', readonly=False)
    
class pos_config(models.Model):
    _inherit = 'pos.config' 

    multi_receipt_count = fields.Integer('Multi Receipt Count', default=1)



