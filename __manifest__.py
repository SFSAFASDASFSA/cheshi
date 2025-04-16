# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'myaccounting',
    'version': '1.0',
    'depends': ['base', 'account', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/myaccounting_type_views.xml',
        'views/myaccounting_property_views.xml',
        'views/myaccounting_tag_views.xml',
        'views/myaccounting_offer_views.xml',
        'views/myaccounting_menu_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
