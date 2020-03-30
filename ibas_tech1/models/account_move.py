# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, safe_eval, date_utils, email_split, email_escape_char, email_re
from odoo.tools.misc import formatLang, format_date

from datetime import date, timedelta
from itertools import groupby
from stdnum.iso7064 import mod_97_10
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import json
import re
import logging
import psycopg2

_logger = logging.getLogger(__name__)


class IBASMoveInvoice(models.Model):
    _inherit = 'account.move'

    name = fields.Char(string='Number', required=True,
                       readonly=False, copy=False, default='/')

    tin = fields.Char('Tin')
    business_name = fields.Char('Business Name/Style')
    prepared_by = fields.Char('Prepared By:')
    approved_by = fields.Char('Approved By:')
    received_by = fields.Char('Received By:')


class IBASAccountLine(models.Model):
    _inherit = 'account.move.line'
    discount_incurrency = fields.Float(string='Discount Amount')

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        ''' This method is used to compute 'price_total' & 'price_subtotal'.

        :param price_unit:  The current price unit.
        :param quantity:    The current quantity.
        :param discount:    The current discount.
        :param currency:    The line's currency.
        :param product:     The line's product.
        :param partner:     The line's partner.
        :param taxes:       The applied taxes.
        :param move_type:   The type of the move.
        :return:            A dictionary containing 'price_subtotal' & 'price_total'.
        '''
        res = {}

        # Compute 'price_subtotal'.
        price_unit_wo_discount = price_unit * (1 - (discount / 100.0))
        # price_unit_wo_discount = price_unit_wo_discount - self.discount_incurrency
        subtotal = quantity * price_unit_wo_discount

        # Compute 'price_total'.
        if taxes:
            taxes_res = taxes._origin.compute_all(price_unit_wo_discount,
                                                  quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
            res['price_subtotal'] = taxes_res['total_excluded']
            res['price_total'] = taxes_res['total_included']
        else:
            res['price_total'] = res['price_subtotal'] = subtotal
        return res
