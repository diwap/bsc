# -*- coding: utf-8 -*-

{
    'name': "BI Theme",
    'author': "BI Solutions",
    'website': "",
    'sequence': 1,
    'installable': True,
    'application': True,
    'auto_install': False,
    'summary': u"""
        Backend/AppSwither/Sidebar.
        """,
    'description': u"""
		Backend theme for Odoo 10.0 community edition.
		
		Beautiful login page.
		
		it's very efficient when it runs in different terminals
		
		user/pass: demo
    """,
    "category": "Themes/Backend",
    'version': '10.0.1.1',
    'depends': [
        'web',
    ],
    'data': [
        'templates/assets.xml',
        'templates/backend.xml',
        'views/page_login.xml',
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'images': ['images/main_screenshot.png'],
    'currency': 'EUR',
    'price': 99,
}
