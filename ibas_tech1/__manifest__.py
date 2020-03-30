# -*- coding: utf-8 -*-
{
    'name': "ibas_tech1",

    'summary': """
       IBAS Customizations for Tech1""",

    'description': """
        Long description of module's purpose
    """,

    'author': "IBAS",
    'website': "http://www.ibasuite.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale', 'sales_team', 'account', 'web', 'purchase', 'purchase_stock', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/ibas_tech1_security.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/view_order_form.xml',
        'views/view_move_form.xml',
        'views/purchase_order.xml',
        'views/account_payment.xml',
        'views/stock_picking.xml',
        'views/cus_account_move_views.xml',
        'report/report_templates.xml',
        'report/purchase_report.xml',
        'report/report_deliveryslip.xml',
        'report/report_cus_account_move.xml',
        'report/report_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
