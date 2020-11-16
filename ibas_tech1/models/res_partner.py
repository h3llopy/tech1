

# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    user_id = fields.Many2one('res.users', string='Salesperson',
                              help='The internal user in charge of this contact.', default=lambda self: self.env.user and self.env.user.id or False)
