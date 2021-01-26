# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Pengeluaran',
    'version': '12.0.1.0.0',
    'summary': 'DJBC Laporan Pengeluaran Fasilitas TPB dan Non Fasilitas',
    'description': 'DJBC Laporan Pengeluaran Fasilitas TPB dan Non Fasilitas',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
        'security/ir.model.access.csv',
	'wizards/nofas_keluar_wiz.xml',	
        'views/nofas_keluar.xml',
        'views/menu.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
