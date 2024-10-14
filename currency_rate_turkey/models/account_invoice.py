# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def action_move_create(self):
        """
        This is necessary to use proper currency rate on move creation
        """
        new_context = self._context.copy()
        if self.partner_id.property_rate_field != "rate" and not self.use_custom_rate:
            new_context.update(
                {
                    "rate_type": self.partner_id.property_rate_field,
                }
            )
        return super(
            AccountInvoice, self.with_context(new_context)
        ).action_move_create()

    @api.model
    def create(self, vals):
        """
        Use proper currency rate on invoice creation
        """
        if vals.get("partner_id"):
            partner = self.env["res.partner"].browse(vals["partner_id"])
            if partner and partner.property_rate_field != "rate":
                self = self.with_context(rate_type=partner.property_rate_field)
        return super(AccountInvoice, self).create(vals)
