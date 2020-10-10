from odoo import fields, models, api


class IBASCrmLead(models.Model):
    _inherit = 'crm.lead'

    def _get_partner_id_domain(self):
        user = self.env.user
        if user and (user.has_group('ibas_tech1.group_ibas_tech1_dealer')):
            domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)]
        else:
            domain = ['|', ('company_id', '=', False), ('company_id', '=', user.company_id.id)]

        return domain

    partner_id = fields.Many2one('res.partner', string='Customer', tracking=10, index=True,
                                 domain=_get_partner_id_domain,
                                 help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")

