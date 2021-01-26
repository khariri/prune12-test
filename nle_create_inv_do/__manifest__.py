# -*- coding: utf-8 -*-
{
    'name': 'NLE Create DO Invoice',
    'version': '12.0.1.0.0',
    'summary': 'NLE Create DO Invoice',
    'description': 'NLE Create DO Invoice',
    'category': 'Extra Tools',
    'author': 'Oktovan Rezman',
    'website': '-',
    # 'license': 'AGPL',
    'depends': ['djbc'],
    'data': [
	'wizards/create_inv_do_wiz.xml',
        'views/djbc_docs.xml',
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,
    # 'external_dependencies': {
    #    'python': [''],
    # }
}
