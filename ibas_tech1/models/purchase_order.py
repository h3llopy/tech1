# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)
READONLY_STATES = {
        'purchase': [('readonly', True)],
        'done': [('readonly', True)],
        'cancel': [('readonly', True)],
    }
class IBASPO(models.Model):
    _inherit = 'purchase.order'
    project_name = fields.Char(string='Project Name')   

    prepared_by = fields.Many2one('res.users', string='Prepared By')
    checked_by = fields.Many2one('res.users', string='Checked By')
    approved_by = fields.Many2one('res.users', string='Approved By')

    prepared_by_signature = fields.Char(string='Prepared By Signature')
    checked_by_signature = fields.Char(string='Checked By Signature')
    approved_by_signature = fields.Char(string='Approved By Signature')
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, states=READONLY_STATES, change_default=True, domain="[(1, '=', 1)]", tracking=True, help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
