# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class AccountPaymentIbas(models.Model):
    _inherit = 'account.payment'
    
    description = fields.Text(string='Description')
    cv_no = fields.Char(string='CV No.')
    check_no = fields.Char(string='Check No.')
    prepared_by = fields.Char(default='CMC')
    review_by = fields.Char(default='JRS')
    approved_by = fields.Char(default='JEM')
    remarks = fields.Text()