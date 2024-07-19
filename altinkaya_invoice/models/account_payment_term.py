# Copyright 2024 Ahmet Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _


class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term"

    convert_invoice_to_try = fields.Boolean(string="Convert Invoice to TRY")
