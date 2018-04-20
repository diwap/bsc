# -*- coding: utf-8 -*-

{
    'name': "Tea Backend Theme",
    'author': "Rain Studio",
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
    'live_test_url': 'http://54.71.162.151:8069/web?db=tea',
    'images': ['images/main_screenshot.png'],
    'currency': 'EUR',
    'price': 99,
}
