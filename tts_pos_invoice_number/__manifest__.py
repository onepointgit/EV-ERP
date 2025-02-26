# -*- coding: utf-8 -*-
{
    "name": "Invoice Number on POS Receipt and POS Invoice on Receipt",
    'version': '1.0',
    'author': 'Truets Tech Solutions',
    'category': 'Point of Sale',
    'depends': ['point_of_sale'],
    'summary': 'This module helps you to show invoice number on pos receipt | Invoice on Receipt | Invoive Number on POS Receipt | POS Invoice Receipt | Invoice number in pos ticket',
    'description': """
- Odoo Invoice number on pos receipt
    """,
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'tts_pos_invoice_number/static/src/js/pos_store.js',
            'tts_pos_invoice_number/static/src/xml/**/*',
        ],
    },
    'application': True,
    'installable': True,
    "license": "LGPL-3",
    'live_test_url': 'https://youtu.be/svxHGEmeP58',
    "images":["static/description/Banner.png"],
}
