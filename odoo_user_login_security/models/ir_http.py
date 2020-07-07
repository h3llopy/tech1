# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from logging import getLogger
from os import utime
from os.path import getmtime
from time import time

from odoo import models,SUPERUSER_ID
from odoo.http import request,root


_logger = getLogger(__name__)


class IrHttp(models.AbstractModel):
	_inherit = 'ir.http'

	@classmethod
	def _authenticate(cls, auth_method='user'):
		res = super(IrHttp, cls)._authenticate(auth_method=auth_method)
		cls._timeout_check()
		return res

	@classmethod
	def _timeout_check(cls):
		if request.httprequest.path in request.env['ir.config_parameter']._get_urls():
			return

		if not request.uid or request.uid == SUPERUSER_ID:
			return

		# Calculate deadline
		delay = request.env['ir.config_parameter']._get_delay()
		deadline = time() - delay if delay > 0 else False

		# Check if past deadline
		expired = False
		path = root.session_store.get_session_filename(request.session.sid)
		if deadline:
			try:
				expired = getmtime(path) < deadline
			except OSError:
				_logger.debug('Exception reading session file modified time.')

		# If timeout, terminate
		if expired and request.session.db and request.session.uid:
			request.session.logout(keep_db=True,state='timed_out')

		# Else, update session last modified/access times
		else:
			try:
				utime(path, None)
			except OSError:
				_logger.debug('Exception updating session file access/modified times.')
