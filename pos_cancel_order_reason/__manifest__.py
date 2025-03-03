# -*- coding: utf-8 -*-

{
    'name': 'POS Cancel Order Reason',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': '',
    'summary': 'This module allows you to choose reason for canceling order',
    'description': """

=======================

This module allows you to choose reason for canceling order
""",
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_order_cancel_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_cancel_order_reason/static/src/**/*',
        ],
    },
    'images': [
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
}
