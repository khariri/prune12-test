# -*- coding: utf-8 -*-
{
    'name': 'NLE Create SP2 Invoice',
    'version': '12.0.1.0.0',
    'summary': 'NLE Create SP2 Invoice',
    'description': 'NLE Create SP2 Invoice',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
        'wizards/create_inv_sp2_wiz.xml',
        'views/djbc_docs.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
