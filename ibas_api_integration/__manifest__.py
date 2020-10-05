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

    'depends': ['base','contacts', 'crm'],

    # always loaded
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Data
        'data/ir_cron_data.xml',
        'data/res_users_data.xml',
        'data/res_groups_data.xml',

        # Views
        'views/res_partner_ext_views.xml',
        'views/crm_lead_ext_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
