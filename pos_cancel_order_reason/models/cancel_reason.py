# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosCancelReason(models.Model):
    _name = "pos.order.cancel.reason"
    _description = "POS Order cancel reason"
    _rec_name = 'name'
    _order = "id"

    name = fields.Char('Reason')

    @api.model
    def _load_pos_data_fields(self):
        return ['id', 'name']

    @api.model
    def _load_pos_data_domain(self):
        return []

    def _load_pos_data(self, data):
        domain = self._load_pos_data_domain()
        fields = self._load_pos_data_fields()
        return {
            'data': self.search_read(domain, fields, load=False),
            'fields': self._load_pos_data_fields(),
        }


class PosSession(models.Model):
    _inherit = 'pos.session'

    @api.model
    def _load_pos_data_models(self, config_id):
        data = super()._load_pos_data_models(config_id)
        data += ['pos.order.cancel.reason']
        return data


class PosOrder(models.Model):
    _inherit = "pos.order"

    reason_id = fields.Many2one('pos.order.cancel.reason', string="Cancel Reason")