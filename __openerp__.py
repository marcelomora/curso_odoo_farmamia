# -*- coding: utf-8 -*-
{
    'name': 'My module',
    'summary': 'Training Odoo module',
    'description': """
Training Module
===========================
An Odoo development training module
---------------------------
First module made by training sessions for Farmacias Mia
- First create __init__.py
- Then create __openerp__.py
    """,
    'author': "Marcelo Mora",
    'licence': 'AGPL-3',
    'website': 'http://farmaciasmia.com',
    'category': 'Training',
    'version': '9.0.1.0.0',
    'depends': ['base'],
    'data': [
         'views/library_book.xml',
         'views/library_customers.xml',
         'views/partner_view.xml',
         'security/ir.model.access.csv',
         'security/groups.xml',
    ]
}
