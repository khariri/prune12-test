# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Mutasi',
    'version': '12.0.1.0.0',
    'summary': 'DJBC Laporan Mutasi',
    'description': 'DJBC Laporan Mutasi',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
        'security/ir.model.access.csv',
        'views/mutasi.xml',
	'reports/report.xml',
        'wizards/mutasi_wiz.xml',
        'views/menu.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
