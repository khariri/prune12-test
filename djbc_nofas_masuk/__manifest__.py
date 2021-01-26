# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Pemasukan',
    'version': '12.0.1.0.0',
    'summary': 'DJBC Laporan Pemasukan Fasilitas TPB dan Non Fasilitas',
    'description': 'DJBC Laporan Pemasukan Fasilitas TPB dan Non Fasilitas',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
        'security/ir.model.access.csv',
	'wizards/nofas_masuk_wiz.xml',	
        'views/nofas_masuk.xml',
        'views/menu.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
