# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Tech1ResUser(models.Model):

    _inherit = 'res.users'

    # location_id = fields.Many2one(
    #    'stock.location', string="Location", domain="[('usage','=','internal')]")

    warehouse_id = fields.Many2one(
        'stock.warehouse', string="Warehouse")

    def write(self, values):
        values = self._remove_reified_groups(values)
        res = super(Tech1ResUser, self).write(values)
        group_warehouse = self.env.ref(
            'ibas_tech1.group_stock_assigned_warehouses_only', False)
        if group_warehouse and 'warehouse_id' in values:
            self.write({'groups_id': [(3, group_warehouse.id)]})
            for user in self:
                if len(user.warehouse_id) <= 0 and user.id in group_warehouse.users.ids:
                    user.write({'groups_id': [(4, group_warehouse.id)]})
                elif len(user.warehouse_id) >= 1 and user.id not in group_warehouse.users.ids:
                    user.write({'groups_id': [(4, group_warehouse.id)]})
        return res
