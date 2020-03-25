# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from openerp import api, models, fields
from openerp.exceptions import Warning

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
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
    def _get_max_credit_limit_allow(self):
        self.max_credit_limit_allow = self.partner_id.max_credit_limit_allow                                                                
            
    @api.one        
    def _get_need_check_credit_limit(self):
        self.need_check_credit_limit = False
        if self.payment_mode_id.id>0:
            #account_payment_mode_ids_need_check_credit_limit
            account_payment_mode_ids_need_check_credit_limit = []
            items_split = self.env['ir.config_parameter'].sudo().get_param('account_payment_mode_ids_need_check_credit_limit').split(",")
            for item_split in items_split:
                account_payment_mode_ids_need_check_credit_limit.append(int(item_split))            
            #check
            if self.payment_mode_id.id in account_payment_mode_ids_need_check_credit_limit:                    
                self.need_check_credit_limit = True