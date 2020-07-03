# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models

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
            account_invoice_ids = self.env['account.invoice'].search([
                ('partner_id', '=', self.id),
                ('type', '=', 'out_invoice'),
                ('state', '=', 'open'),
                ('payment_mode_id.use_to_calculate_max_credit_limit_allow', '=', True)
            ])
            if len(account_invoice_ids)>0:
                for account_invoice_id in account_invoice_ids:
                    self.max_credit_limit_allow = self.max_credit_limit_allow - account_invoice_id.residual
                    
            sale_order_ids = self.env['sale.order'].search([
                ('partner_id', '=', self.id),
                ('amount_total', '>', 0),
                ('state', 'in', ('sale', 'done')),
                ('payment_mode_id.use_to_calculate_max_credit_limit_allow', '=', True),
                ('invoice_status', '=', 'to invoice'),
            ])                    
            if len(sale_order_ids)>0:
                for sale_order_id in sale_order_ids:
                    self.max_credit_limit_allow = self.max_credit_limit_allow - sale_order_id.amount_total    