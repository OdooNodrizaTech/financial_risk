# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Monetary(
        string='Limite de credito',
        track_visibility='onchange' 
    )
    max_credit_limit_allow = fields.Monetary(
        compute='_get_max_credit_limit_allow',        
        store=False 
    )
    
    @api.one        
    def _get_max_credit_limit_allow(self):
        self.max_credit_limit_allow = self.credit_limit
        
        if self.max_credit_limit_allow>0:
            #account_payment_mode_ids_need_check_credit_limit
            account_payment_mode_ids_sepa_credit = []
            items_split = self.env['ir.config_parameter'].sudo().get_param('account_payment_mode_ids_sepa_credit').split(",")
            for item_split in items_split:
                account_payment_mode_ids_sepa_credit.append(int(item_split))
            #account_invoice                                            
            account_invoice_ids = self.env['account.invoice'].search([
                ('partner_id', '=', self.id),
                ('type', '=', 'out_invoice'),
                ('state', '=', 'open'),
                ('payment_mode_id', 'in', account_payment_mode_ids_sepa_credit)
            ])
            if len(account_invoice_ids)>0:
                for account_invoice_id in account_invoice_ids:
                    self.max_credit_limit_allow = self.max_credit_limit_allow - account_invoice_id.residual
                    
            sale_order_ids = self.env['sale.order'].search([
                ('partner_id', '=', self.id),
                ('amount_total', '>', 0),
                ('state', 'in', ('sale', 'done')),
                ('payment_mode_id', 'in', account_payment_mode_ids_sepa_credit),
                ('invoice_status', '=', 'to invoice'),
            ])                    
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    self.max_credit_limit_allow = self.max_credit_limit_allow - sale_order_id.amount_total    