# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'
    _order = 'position'
    
    use_to_calculate_max_credit_limit_allow = fields.Boolean(
        string='Use to Max credit',
        help='Si esta activo se usara este modo de pago para las facturas que lo tengan a la hora de calcular el riesgo vivo del cliente',
        default=True
    )