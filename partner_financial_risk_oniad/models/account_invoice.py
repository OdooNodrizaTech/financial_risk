# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    invoice_with_risk = fields.Boolean(
        string='Invoice With Risk' 
    )
    
    @api.multi
    def action_invoice_open(self):
        return_object = super(AccountInvoice, self).action_invoice_open()
        #oniad_payment_mode_id_with_credit_limit        
        oniad_payment_mode_id_with_credit_limit = int(self.env['ir.config_parameter'].sudo().get_param('oniad_payment_mode_id_with_credit_limit'))
        #operations
        for obj in self:
            #Si es giro ventas la marcamos como que la factura tiene riesgo
            if obj.payment_mode_id.id==oniad_payment_mode_id_with_credit_limit:
                obj.invoice_with_risk = True
            '''(Ahora mismo no entiendo el sentido de esto)
            if obj.partner_id.credit_limit>0:
                obj.invoice_with_risk = True
            else:
                obj.invoice_with_risk = False
            '''                           
        #return                            
        return return_object