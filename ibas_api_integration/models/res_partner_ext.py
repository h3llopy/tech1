# -*- coding: utf-8 -*-

import logging
import requests
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class IBASResPartnerExt(models.Model):
    _inherit = 'res.partner'

    api_synced = fields.Boolean(string='API Synced?')
    number_license = fields.Integer(string='Number License')
    license_duration = fields.Integer(string='License Duration')

    def _synchronize_created_user(self):
        post_url = 'https://us-central1-quicktalk-test.cloudfunctions.net/account/new'

        # Get all contacts to sync
        contact_ids = self.env['res.partner'].search([('api_synced', '=', False)])

        for contact in contact_ids:
            data = {
                "account_id": contact.id,
                "account_name": contact.name,
                "number_license": contact.number_license,
                "license_duration": contact.license_duration
            }
            response = requests.post(post_url, data=data)
            if response.status_code == 200:
                contact.write({'api_synced': True})

