# -*- coding: utf-8 -*-
{
    'name': 'Balance Sheet Excel',
    'version': '12.0.1.0.0',
    'summary': 'Balance Sheet Excel',
    'description': 'Balance Sheet Excel',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['accounting_pdf_reports'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/pr_balance_sheet.xml',
        'wizards/pr_balance_sheet_wiz.xml',
        'views/menu.xml',
        'reports/report.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
