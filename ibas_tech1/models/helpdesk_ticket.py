# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    user_id = fields.Many2one(
        'res.users', string='Assigned to', track_visibility='onchange')
    member_ids = fields.Many2many('res.users', related='team_id.member_ids')

#     @api.onchange('team_id','user_id')
#     def _on_change_team_id(self):
#         member_ids = self.team_id.mapped('member_ids').ids
#         return  {'domain': {'user_id': [('id', 'in', member_ids)]}}
