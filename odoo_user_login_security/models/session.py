# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from requests import get

from odoo import api,fields,models,exceptions
from odoo.http import request,root


class UserSession(models.Model):
	_name        = 'session.session'
	_description = 'Session'
	_rec_name    = 'user_id'
	_order       = 'active desc,date_logout desc,date_login desc'

	def _compute_duration(self):
		for rec in self:
			if rec.date_logout:
				rec.duration = rec.date_logout - rec.date_login

	def _compute_if_current(self):
		for rec in self:
			rec.is_current = rec.session_id == request.session.sid and rec.user_id == request.env.user and rec.active

	@api.depends('ip')
	def _compute_country_id(self):
		for rec in self:
			response = get('http://api.petabyet.com/geoip/%s'%rec.ip)
			if response:
				code = response.json().get('country_code')
				if code:
					rec.country_id = self.env['res.country'].search([('code','=',code)]).id

	is_current = fields.Boolean(compute=_compute_if_current)
	active     = fields.Boolean('Logged',required=True,index=True)
	session_id = fields.Char('Session ID',size=100)
	ip         = fields.Char('Remote IP',size=15)
	platform   = fields.Selection(
		selection=[
			('android','Android'),
			('chromeos','ChromeOS'),
			('iphone','iPhone'),
			('ipad','iPad'),
			('macos','MacOS'),
			('windows','Windows'),
			('linux','Linux'),
			('other','Other Platforms'),
		],
		default='other',
	)
	browser = fields.Selection(
		selection=[
			('chrome','Google Chrome'),
			('edge','Microsoft Edge'),
			('firefox','Mozzila Firefox'),
			('msie','Internet Explorer'),
			('opera','Opera'),
			('safari','Safari'),
			('other','Other Browsers'),
		],
		default='other',
	)
	browser_version = fields.Char()
	user_agent      = fields.Char()
	date_login      = fields.Datetime('Login',required=True)
	date_logout     = fields.Datetime('Logout',inverse=_compute_duration)
	duration        = fields.Char('Duration (HH:MM:SS)')
	user_id         = fields.Many2one('res.users','User',ondelete='cascade',required=True)
	state           = fields.Selection(
		selection= [
			('logged_in','Logged In'),
			('logged_out','Logged Out'),
			('timed_out','Timeout'),
			('terminated','Terminated'),
			('error','Login Failed'),
		],
		default  = 'logged_in',
		required = True,
		readonly = True,
	)
	country_id = fields.Many2one('res.country', compute=_compute_country_id, store=True)

	_sql_constraints = [('session_id_unique','unique(session_id)','Duplicate session id detected')]

	@api.model
	def save_session(self,uid=False,state=False):
		forwarded_for = request.httprequest.headers.environ.get('HTTP_X_FORWARDED_FOR')
		if forwarded_for:
			ip = forwarded_for.split(',')[0]
		else:
			ip = request.httprequest.headers.environ['REMOTE_ADDR']
		user_agent = request.httprequest.user_agent
		session = request.env['session.session'].sudo().create(
			{
				'user_id'        : uid or request.uid,
				'session_id'     : state != 'error' and request.session.sid,
				'date_login'     : fields.datetime.utcnow(),
				'ip'             : ip,
				'platform'       : user_agent.platform,
				'browser'        : user_agent.browser,
				'browser_version': user_agent.version,
				'user_agent'     : user_agent.string,
				'state'          : state or 'logged_in',
				'active'         : state != 'error' and True,
			}
		)
		try:
			self._cr.commit()
		except Exception:
			self.sudo()._cr.commit()
		return session

	def terminate(self):
		for rec in self:
			if rec.active and not rec.is_current:
				session = root.session_store.get(rec.session_id)
				session.logout(keep_db=True,state='terminated')
				root.session_store.delete(session)

	def _on_logout(self,state):
		self.sudo().write(
			{
				'active'     : False,
				'date_logout': fields.datetime.utcnow(),
				'state'      : state,
			}
		)
		self._cr.commit()

	@api.model
	def clear_inactive_sessions(self):
		days_before = self.env['ir.config_parameter'].get_param(
			'odoo_user_login_security.clear_inactive_session_after',
			90,
		)
		days_before = fields.datetime.utcnow() + \
			fields.date_utils.relativedelta(days=-int(days_before))
		self.search([('active','=',False),('date_logout','<',days_before)]).unlink()

	def send_login_email(self, status):
		self.ensure_one()
		if self.user_id.email:
			get_param = self.env['ir.config_parameter'].sudo().get_param
			mail_template = False
			if status == 'suspicious' and get_param('odoo_user_login_security.send_suspicious_login_email'):
				mail_template = self.env.ref('odoo_user_login_security.mail_login_suspicious')
			elif status == 'error' and get_param('odoo_user_login_security.send_failed_login_email'):
				mail_template = self.env.ref('odoo_user_login_security.mail_login_failure')
			if mail_template:
				mail_template.send_mail(self.id,force_send=True)
