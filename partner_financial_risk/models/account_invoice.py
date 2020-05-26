# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)

from odoo import api, models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    invoice_with_risk = fields.Boolean(
        string='Invoice With Risk',
        default=False
    )

    @api.multi
    def action_invoice_open(self):
        return_object = super(AccountInvoice, self).action_invoice_open()
        # operations (Need to cesce)
        for obj in self:
            if obj.type=='out_invoice':
                if obj.payment_mode_id.id>0:
                    if obj.payment_mode_id.payment_method_id.id>0:
                        if obj.payment_mode_id.payment_method_id.code == 'sepa_direct_debit':
                            obj.invoice_with_risk = True
        # return
        return return_object