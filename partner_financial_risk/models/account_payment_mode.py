# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'
    _order = 'position'
    
    use_to_calculate_max_credit_limit_allow = fields.Boolean(
        string='Use to Max credit',
        help="If it is active, this payment method will be used for the invoices they have when calculating the customer's living risk",
        default=True
    )