# -*- coding: utf-8 -*-

import logging
import requests
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
_logger = logging.getLogger(__name__)


class IBASAPI(models.AbstractModel):
    _name = 'ibas.api'
    _description = 'IBAS API'

    @api.model
    def update_contact(self, data):
        contact_id = data.get('contact_id') and data.pop('contact_id') or False
        if not contact_id:
            raise ValidationError('Contact id is required.')

        contact_id = self.env['res.partner'].sudo().browse(contact_id)
        result = contact_id.sudo().write(data)
        return True

    @api.model
    def delete_contact(self, data):
        contact_id = data.get('contact_id')
        if not contact_id:
            raise ValidationError('Contact id is required.')

        contact_id = self.env['res.partner'].sudo().search([('id', '=', contact_id)])
        if contact_id:
            contact_id.sudo().unlink()
        else:
            raise ValidationError('Contact does not exist.')
        return True