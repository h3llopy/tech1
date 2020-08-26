# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class Tech1SaleOrder(models.Model):

    _inherit = 'sale.order'

    @api.model
    def _default_warehouse_id(self):
        company = self.env.company.id
        flag = self.env['res.users'].has_group(
            'ibas_tech1.group_ibas_tech1_dealer')
        if flag:
            warehouse_ids = self.env['stock.warehouse'].search(
                [('id', '=', self.env.user.warehouse_id.id)], limit=1)
        else:
            warehouse_ids = self.env['stock.warehouse'].search(
                [('company_id', '=', company)], limit=1)
        return warehouse_ids

    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: ['|', ('groups_id', 'in', self.env.ref('sales_team.group_sale_salesman').id), ('groups_id', 'in', self.env.ref('ibas_tech1.group_ibas_tech1_dealer').id)])

    warehouse_id = fields.Many2one(
        'stock.warehouse', string='Warehouse',
        required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default=_default_warehouse_id, check_company=True)


class Tech1Sale(models.Model):

    _inherit = 'sale.order.line'

    discount_incurrency = fields.Float(string='Discount Amount')

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'discount_incurrency')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price = price - line.discount_incurrency
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        return {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit - self.discount_incurrency,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            'discount_incurrency': self.discount_incurrency,
        }
