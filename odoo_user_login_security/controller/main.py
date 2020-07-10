# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from werkzeug import utils

from odoo import fields, http
from odoo.http import request

from odoo.addons.web.controllers import main

class Home(main.Home):
	@http.route('/web/login',type='http',auth='public')
	def web_login(self,redirect=None,**kw):
		login = kw.get('login')
		user = False
		sessions = False
		if login:
			user = request.env['res.users'].sudo().search([('login','=',login)])

		if user:
			get_param = request.env['ir.config_parameter'].sudo().get_param
			is_admin = request.env.ref('base.user_admin') == user

			multiple_sessions_allowed = get_param('odoo_user_login_security.allow_multiple_session','yes') == 'yes'
			force_login = get_param('odoo_user_login_security.override_past_session','yes') == 'yes'
			password_lifetime = int(get_param('odoo_user_login_security.password_lifetime'))
			reset_password_redirect = get_param('odoo_user_login_security.password_change_ask') == 'force'

			# NOTE: handling for simultaneous sessions
			if not multiple_sessions_allowed:
				sessions = request.env['session.session'].sudo().search([('user_id','=',user.id)])
				if sessions:
					if is_admin or force_login:
						terminate_past_session = True
					else:
						values = request.params.copy()
						values['error'] = '''
							Someone logged into this account from another device or browser.
							Your current session is terminated.
						'''
						request.params['login_success'] = False
						return request.render('web.login',values)

			#NOTE: If password too old, handle it accordingly
			if password_lifetime:
				password_lifetime = fields.date_utils.relativedelta(days=password_lifetime)
				last_password_reset = user.partner_id.last_password_reset or user.partner_id.create_date
				is_password_too_old = last_password_reset + password_lifetime < fields.datetime.utcnow()
				if is_password_too_old:
					if not reset_password_redirect or is_admin:
						recommend_password_update = True
					else:
						request.params['login_success'] = False
						return utils.redirect('web/reset_password?',303)

		res = super(Home,self).web_login(redirect,**kw)
		if user and res.status_code in [200,303]:
			user.partner_id.sudo().update_password_reset_attempt_count(reset=True)
			if locals().get('terminate_past_session'):
				sessions.terminate()
			if locals().get('recommend_password_update'):
				request.env.user.recommend_password_update()
		return res

	@http.route('/web/session/logout',type='http',auth='none')
	def logout(self,redirect='/web'):
		if request.env.registry.get('session.session'):
			request.session.logout(keep_db=True,state='logged_out')
		else:
			request.session.logout(keep_db=True)
		return utils.redirect(redirect,303)
