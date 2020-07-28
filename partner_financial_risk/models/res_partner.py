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
    @api.depends('partner_id')
    def _compute_max_credit_limit_allow(self):
        self.ensure_one()
        if self.partner_id:
            self.max_credit_limit_allow = self.credit_limit
            if self.max_credit_limit_allow > 0:
                # account_invoices
                items = self.env['account.invoice'].search([
                    ('partner_id', '=', self.id),
                    ('type', '=', 'out_invoice'),
                    ('state', '=', 'open'),
                    (
                        'payment_mode_id.use_to_calculate_max_credit_limit_allow',
                        '=',
                        True
                    )
                ])
                if items:
                    for item in items:
                        self.max_credit_limit_allow = \
                            self.max_credit_limit_allow - item.residual
                # sale_orders
                items = self.env['sale.order'].search([
                    ('partner_id', '=', self.id),
                    ('amount_total', '>', 0),
                    ('state', 'in', ('sale', 'done')),
                    (
                        'payment_mode_id.use_to_calculate_max_credit_limit_allow',
                        '=',
                        True)
                    ,
                    ('invoice_status', '=', 'to invoice'),
                ])
                if items:
                    for item in items:
                        self.max_credit_limit_allow = \
                            self.max_credit_limit_allow - item.amount_total
