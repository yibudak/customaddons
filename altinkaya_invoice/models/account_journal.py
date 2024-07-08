'''
Created on Feb 14, 2020

@author: cq
'''
from odoo import fields, models, api

class AccountJournal(models.Model):
    _inherit = "account.journal"

    name = fields.Char(string='Journal Name', required=True, translate=True)

    def _default_outbound_payment_methods(self):
        all_out = self.env["account.payment.method"].search(
            [("payment_type", "=", "outbound")]
        )
        return all_out

    def _default_inbound_payment_methods(self):
        method_info = self.env[
            "account.payment.method"
        ]._get_payment_method_information()
        unique_codes = tuple(
            code for code, info in method_info.items() if info.get("mode") == "unique"
        )
        all_in = self.env["account.payment.method"].search(
            [
                ("payment_type", "=", "inbound"),
                ("code", "not in", unique_codes),  # filter out unique codes
            ]
        )
        return all_in

    @api.constrains("company_id")
    def company_id_account_payment_mode_constrains(self):
        for journal in self:
            mode = self.env["account.payment.mode"].search(
                [
                    ("fixed_journal_id", "=", journal.id),
                    ("company_id", "!=", journal.company_id.id),
                ],
                limit=1,
            )
            if mode:
                raise ValidationError(
                    _(
                        "The company of the journal %(journal)s does not match "
                        "with the company of the payment mode %(paymode)s where it is "
                        "being used as Fixed Bank Journal.",
                        journal=journal.name,
                        paymode=mode.name,
                    )
                )
            mode = self.env["account.payment.mode"].search(
                [
                    ("variable_journal_ids", "in", [journal.id]),
                    ("company_id", "!=", journal.company_id.id),
                ],
                limit=1,
            )
            if mode:
                raise ValidationError(
                    _(
                        "The company of the journal  %(journal)s does not match "
                        "with the company of the payment mode  %(paymode)s where it is "
                        "being used in the Allowed Bank Journals.",
                        journal=journal.name,
                        paymode=mode.name,
                    )
                )

    outbound_payment_method_ids = fields.Many2many(
        'account.payment.method',
        'account_journal_outbound_payment_rel',
        'journal_id', 'payment_method_id',
        string='Outbound Payment Methods',
        default=_default_outbound_payment_methods)
    inbound_payment_method_ids = fields.Many2many(
        'account.payment.method',
        'account_journal_inbound_payment_rel',
        'journal_id', 'payment_method_id',
        string='Inbound Payment Methods',
        default=_default_inbound_payment_methods)

    at_least_one_inbound = fields.Boolean(
        string='Has Inbound Payment Method',
        compute='_compute_at_least_one_inbound'
    )

    @api.depends('inbound_payment_method_ids')
    def _compute_at_least_one_inbound(self):
        for journal in self:
            journal.at_least_one_inbound = bool(journal.inbound_payment_method_ids)

