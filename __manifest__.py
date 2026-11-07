{
    'name': 'Customer Billing Note',
    'version': '18.0.1.1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Generate and manage customer billing notes in Odoo 18',
    'author': 'Peach Lambda Solutions',
    'website': 'https://peachlambda.com',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/billing_note_views.xml',
        'report/billing_note_report.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
