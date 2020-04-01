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
            account_payment_mode_ids_need_check_credit_limit_config = self.env['ir.config_parameter'].sudo().get_param('account_payment_mode_ids_need_check_credit_limit')
            if account_payment_mode_ids_need_check_credit_limit_config!=False:
                if ',' in account_payment_mode_ids_need_check_credit_limit_config:
                    items_split = account_payment_mode_ids_need_check_credit_limit_config.split(",")
                    for item_split in items_split:
                        account_payment_mode_ids_need_check_credit_limit.append(int(item_split))
                else:
                    account_payment_mode_ids_need_check_credit_limit.append(int(account_payment_mode_ids_need_check_credit_limit_config))                                    
            #check
            if len(account_payment_mode_ids_need_check_credit_limit)>0:
                if self.payment_mode_id.id in account_payment_mode_ids_need_check_credit_limit:                    
                    self.need_check_credit_limit = True