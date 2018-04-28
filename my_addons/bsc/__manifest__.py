# -*- coding: utf-8 -*-
{
    'name': "bsc",

    'summary': """
        Strategic Planning and Management System""",

    'description': """
        BSC refers to Balance Score Card. The balanced scorecard is a strategy performance management tool – a semi-standard structured report,
        supported by design methods and automation tools, that can be used by managers to keep track of the execution of activities by the 
        staff within their control and to monitor the consequences arising from these actions.
    """,

    'author': "Diwakar Pandey",
    'website': "http://www.linkedin.in/diwap",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'management',
    'version': '11.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/bsc_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/contact_ext.xml',
        'views/bsc_objective.xml',
        'views/bsc_measure.xml',
        'views/bsc_initiative.xml',
        'views/bsc_measuredata.xml',
        # 'views/bsc_recommendation.xml',
        'views/bsc_milestone.xml',
        'views/bsc_action.xml'
    ],
}