# -*- coding: utf-8 -*-
{
    'name': "IBAS API Integration",

    'summary': """
        IBAS API Integration""",

    'description': """
        This modules contains customizations for API integrations
    """,

    'author': "IBAS Software",
    'website': "http://www.ibasuite.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','contacts'],

    # always loaded
    'data': [
        # Security
        # 'security/ir.model.access.csv',

        # Data
        'data/ir_cron_data.xml',

        # Views
        'views/res_partner_ext_views.xml'
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
