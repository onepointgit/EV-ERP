# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    invoice_number = fields.Char(string='Invoice Number', related="account_move.name")
