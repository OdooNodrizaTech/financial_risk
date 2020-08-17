# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class AccountPaymentMode(models.Model):
    _inherit = 'account.payment.mode'

    use_to_calculate_max_credit_limit_allow = fields.Boolean(
        string='Use to Max credit',
        help="If it is active, this payment method will be "
             "used for the invoices they have when calculating "
             "the customer's living risk",
        default=True
    )
