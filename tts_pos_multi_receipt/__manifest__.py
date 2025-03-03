# -*- coding: utf-8 -*-

{
    'name': 'POS Multi Receipt',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 6,
    'author': 'Truets Tech Solutions',
    'summary': 'This module allows you to print one receipt N times',
    'description': """

=======================

This module allows you to print one receipt N times.

""",
    'depends': ['point_of_sale'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'tts_pos_multi_receipt/static/src/**/*',
        ],
    },
    'images': [
        'static/description/receipt.jpg',
    ],
    'installable': True,
    'website': '',
    'auto_install': False,
    'price': 20,
    'currency': 'EUR',
}
