# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models, fields, _
from odoo.exceptions import Warning as UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id_credit_limit = fields.Float(
        compute='_compute_partner_id_credit_limit',
        store=False,
        string='Credit granted'
    )
    need_check_credit_limit = fields.Boolean(
        compute='_compute_need_check_credit_limit',
        store=False
    )
    max_credit_limit_allow = fields.Monetary(
        compute='_compute_max_credit_limit_allow',
        store=False
    )

    @api.onchange('payment_mode_id')
    def change_payment_mode_id(self):
        self._get_need_check_credit_limit()
        self._get_max_credit_limit_allow()

    @api.multi
    @api.depends('partner_id')
    def _compute_partner_id_credit_limit(self):
        self.ensure_one()
        if self.partner_id:
            self.partner_id_credit_limit = self.partner_id.credit_limit

    @api.multi
    @api.depends('partner_id')
    def _compute_need_check_credit_limit(self):
        self.ensure_one()
        if self.partner_id:
            self.max_credit_limit_allow = self.partner_id.max_credit_limit_allow

    @api.multi
    @api.depends('payment_mode_id')
    def _compute_max_credit_limit_allow(self):
        self.ensure_one()
        self.need_check_credit_limit = False
        if self.payment_mode_id:
            if self.payment_mode_id.payment_method_id.code \
                    == 'sepa_direct_debit':
                self.need_check_credit_limit = True

    @api.multi
    def action_confirm(self):
        # check
        allow_confirm = True
        for item in self:
            if item.need_check_credit_limit:
                future_max_credit_limit_allow = \
                    item.max_credit_limit_allow - item.amount_total
                if future_max_credit_limit_allow <= 0:
                    allow_confirm = False
                    raise UserError(_('The sale cannot be confirmed because there is '
                                      'no available credit or the total amount of this '
                                      'sale is greater than the available credit (%s)'
                                      % (str(future_max_credit_limit_allow)))
                                    )
        # allow_confirm
        if allow_confirm:
            return super(SaleOrder, self).action_confirm()
