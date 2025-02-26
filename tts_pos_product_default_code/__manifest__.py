# -*- coding: utf-8 -*-
{
    'name': "POS product internal reference in product list",

    'summary': "Displays the internal reference in the product list and on point-of-sale receipts.",

    'author': "Truets Tech Solutions",
    'category': 'Sales/Point of Sale',
    'version': '18.0.1.0',
    'license': 'OPL-1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['point_of_sale'],

    'data': [
        'views/pos_config_view.xml',
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            '/tts_pos_product_default_code/static/src/js/**/*',
            '/tts_pos_product_default_code/static/src/xml/**/*',
            '/tts_pos_product_default_code/static/src/css/*.css',
        ],
    }
}