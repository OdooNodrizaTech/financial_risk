# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    credit_limit = fields.Monetary(
        string='Credit Limit',
        track_visibility='onchange'
    )
    max_credit_limit_allow = fields.Monetary(
        compute='_compute_max_credit_limit_allow',
        store=False
    )

    @api.multi
    def _compute_max_credit_limit_allow(self):
        for item in self:
            item.max_credit_limit_allow = item.credit_limit
            if item.max_credit_limit_allow > 0:
                # account_invoices
                invoice_ids = self.env['account.invoice'].search([
                    ('partner_id', '=', item.id),
                    ('type', '=', 'out_invoice'),
                    ('state', '=', 'open'),
                    (
                        'payment_mode_id.use_to_calculate_max_credit_limit_allow',
                        '=',
                        True
                    )
                ])
                if invoice_ids:
                    for invoice_id in invoice_ids:
                        item.max_credit_limit_allow = \
                            item.max_credit_limit_allow - invoice_id.residual
                # sale_orders
                order_ids = self.env['sale.order'].search([
                    ('partner_id', '=', item.id),
                    ('amount_total', '>', 0),
                    ('state', 'in', ('sale', 'done')),
                    (
                        'payment_mode_id.use_to_calculate_max_credit_limit_allow',
                        '=',
                        True)
                    ,
                    ('invoice_status', '=', 'to invoice'),
                ])
                if order_ids:
                    for order_id in order_ids:
                        item.max_credit_limit_allow = \
                            item.max_credit_limit_allow - order_id.amount_total
