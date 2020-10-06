# -*- coding: utf-8 -*-

import logging
import requests
from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class IBASCRMLeadExt(models.Model):
    _inherit = 'crm.lead'

    company_email_address = fields.Char(string='Company Email Address')
    business_type = fields.Char(string='Business Type')
    license_duration = fields.Selection(selection=[('yearly', 'Yearly'), ('monthly', 'Monthly')])
    number_of_slots = fields.Integer(string='Number of slots')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    registration_account_license = fields.Char(string='Registration Account License')
    product_id = fields.Many2one(comodel_name='product.product', string='Product')

    @api.model
    def create(self, vals):
        result = super(IBASCRMLeadExt, self).create(vals)

        # Create quotation from CRM lead
        self._generate_quotation(result)
        return result

    @api.onchange('product_id', 'number_of_slots')
    @api.depends('product_id', 'number_of_slots')
    def _compute_total_amount(self):
        for slf in self:
            if slf.product_id:
                slf.total_amount = slf.product_id.lst_price * slf.number_of_slots
            else:
                slf.total_amount = 0.0

    def _generate_quotation(self, lead_id):
        # Create partner
        context = {'active_model': 'crm.lead', 'active_id': lead_id.id}
        quotation_partner_id = self.env['crm.quotation.partner'].with_context(context).create({'action': 'create'})
        quotation_partner_id.action_apply()

        quotation_data = {'partner_id': lead_id.partner_id.id,
                          'partner_invoice_id': lead_id.partner_id.id,
                          'partner_shipping_id': lead_id.partner_id.id,
                          'opportunity_id': lead_id.id}

        # For improvement: Free subscription hardcoded to 10, Make it configurable.
        number_of_quotation = 1
        if lead_id.number_of_slots > 10:
            number_of_quotation += 1

        for x in range(0, number_of_quotation):
            self.env['sale.order'].sudo().create(quotation_data)
