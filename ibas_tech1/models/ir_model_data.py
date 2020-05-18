# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class IRModelData(models.Model):
	_inherit = 'ir.model.data'

	@api.model
	def enable_update(self, module, name):
		self._cr.execute("""UPDATE ir_model_data SET noupdate=False where module=%s and name=%s""", (module,name,))

	@api.model
	def disable_update(self, module, name):
		self._cr.execute("""UPDATE ir_model_data SET noupdate=True where module=%s and name=%s""", (module,name,))
