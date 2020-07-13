# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    partner_id_credit_limit = fields.Float(
        compute='_get_partner_id_credit_limit',
        store=False,
        string='Credit granted'
    )
         
    @api.one        
    def _get_partner_id_credit_limit(self):
        for crm_lead_obj in self:
            crm_lead_obj.partner_id_credit_limit = crm_lead_obj.partner_id.credit_limit                                                            