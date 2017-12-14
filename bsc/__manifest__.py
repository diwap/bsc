# -*- coding: utf-8 -*-
{
    'name': "bsc",

    'summary': """
        Balance Score Card is an indicator""",

    'description': """
        Balance Score Card`
    """,

    'author': "Diwakar Pandey",
    'website': "http://www.linkedin.in/diwap",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'management',
    'version': '11.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}