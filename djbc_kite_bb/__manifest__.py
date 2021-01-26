# -*- coding: utf-8 -*-
{
    'name': 'KITE Laporan Pemasukan Bahan Baku',
    'version': '12.0.1.0.0',
    'summary': 'KITE Laporan Pemasukan Bahan Baku',
    'description': 'KITE Laporan Pemasukan Bahan Baku',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
        'security/ir.model.access.csv',
        'views/kite_masuk_bb.xml',
        'views/menu.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
