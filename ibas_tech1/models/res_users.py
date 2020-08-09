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
