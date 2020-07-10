# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from re import match
from logging import getLogger
from werkzeug import contrib

from odoo import exceptions,http
from odoo.http import root,request
from odoo.tools import config,func


_logger = getLogger(__name__)


class OpenERPSession(http.OpenERPSession):
	def logout(self,keep_db=False,state=False):
		if state and request.registry.get('session.session'):
			session = request.env['session.session'].sudo().search(
				[
					('session_id','=',self.sid),
					('active','=',True),
				]
			)
			if session:
				session._on_logout(state)
		return super(OpenERPSession,self).logout(keep_db=keep_db)

	def authenticate(self, db, login=None, password=None, uid=None):
		try:
			return super(OpenERPSession,self).authenticate(db, login, password, uid)
		except exceptions.AccessDenied:
			if request.registry.get('session.session'):
				uid = request.env.user.search([('login','=',login)]).id
				session = request.env['session.session'].save_session(uid=uid,state='error')
				session.send_login_email(status='error')
			raise


class Root(http.Root):
	@func.lazy_property
	def session_store(self):
		# Setup http sessions
		path = config.session_dir
		_logger.debug('HTTP sessions stored in: %s', path)
		return contrib.sessions.FilesystemSessionStore(path,session_class=OpenERPSession)

	def get_response(self, httprequest, result, explicit_session):
		if request.db and request.registry.get('session.session') and request.params.get('login_success'):
			response = super(Root,self).get_response(httprequest, result, explicit_session)
			known_users = request.httprequest.cookies.get('known_users')
			if known_users:
				try:
					known_users = eval(known_users)
					if isinstance(known_users,int):
						known_users = {known_users}
				except SyntaxError:
					known_users = set(map(int,known_users.split(' ')))
			else:
				known_users = set()
			response.set_cookie('db',request.db)
			session = request.env['session.session'].save_session()
			if request.uid not in known_users:
				session.send_login_email(status='suspicious')
				known_users.add(request.uid)
				response.set_cookie('known_users',str(known_users))
			return response
		return super(Root,self).get_response(httprequest, result, explicit_session)

	def setup_session(self, httprequest):
		res = super().setup_session(httprequest)
		session_id = httprequest.cookies.get('session_id')
		db = httprequest.cookies.get('db')
		is_db_path = match('\/web\?.*db=\w+',httprequest.full_path)
		if session_id and db and not httprequest.session.db and not is_db_path:
			httprequest.session.db = db
		return res


root.session_store = Root().session_store
root.get_response = Root().get_response
root.setup_session = Root().setup_session
