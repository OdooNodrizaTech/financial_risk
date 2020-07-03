# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    partner_id_credit_limit = fields.Float(
        compute='_get_partner_id_credit_limit',
        store=False,
        string='Credito concedido'
    )
    need_check_credit_limit = fields.Boolean(
        compute='_get_need_check_credit_limit',
        store=False 
    )
    max_credit_limit_allow = fields.Monetary(
        compute='_get_max_credit_limit_allow',        
        store=False 
    )
    
    @api.onchange('payment_mode_id')
    def change_payment_mode_id(self):
        self._get_need_check_credit_limit()
        self._get_max_credit_limit_allow()        
    
    @api.one        
    def _get_partner_id_credit_limit(self):
        for sale_order_obj in self:
            sale_order_obj.partner_id_credit_limit = sale_order_obj.partner_id.credit_limit
    
    @api.one        
    def _get_max_credit_limit_allow(self):
        self.max_credit_limit_allow = self.partner_id.max_credit_limit_allow                                                                
            
    @api.one        
    def _get_need_check_credit_limit(self):
        self.need_check_credit_limit = False
        if self.payment_mode_id.id>0:
            if self.payment_mode_id.payment_method_id.code=='sepa_direct_debit':                    
                self.need_check_credit_limit = True
                    
    @api.multi
    def action_confirm(self):
        #check
        allow_confirm = True
        for obj in self:            
            if obj.need_check_credit_limit==True:
                future_max_credit_limit_allow = obj.max_credit_limit_allow - obj.amount_total
                if future_max_credit_limit_allow<=0:
                    allow_confirm = False
                    raise Warning("No se puede confirmar la venta porque no hay credito disponible o el importe total de esta venta es superior al credito disponible ("+str(future_max_credit_limit_allow)+")")        
        #allow_confirm
        if allow_confirm==True:
            return super(SaleOrder, self).action_confirm()                    