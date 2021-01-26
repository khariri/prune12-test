# -*- coding: utf-8 -*-
{
    'name': 'DJBC Laporan Posisi WIP',
    'version': '12.0.1.0.0',
    'summary': 'DJBC Laporan Posisi WIP',
    'description': 'DJBC Laporan Posisi WIP',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
        'security/ir.model.access.csv',
        'views/posisi_wip.xml',
        'wizards/posisi_wip_wiz.xml',
        'views/menu.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
