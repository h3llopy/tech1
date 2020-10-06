# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tech1StockPicking(models.Model):
    _inherit = 'stock.picking'

    pick_line_description = fields.Text(string='Description')
    partner_id = fields.Many2one(
        'res.partner', 'Contact',
        check_company=False,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})
    @api.depends('product_id')
    def updatedesc(self):
        for rec in self:
            rec.pick_line_description = rec.product_id  
    
    
    



# class ibas_tech1(models.Model):
#     _name = 'ibas_tech1.ibas_tech1'
#     _description = 'ibas_tech1.ibas_tech1'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
