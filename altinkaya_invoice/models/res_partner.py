from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _search_due_days(self, operator, value):
        partners = self.search(
            [
                ("property_payment_term_id.line_ids.days", operator, value),
            ],
        )
        return [("id", "in", partners.ids)]

    z_muhasebe_kodu = fields.Char(
        "Zirve Muhasebe kodu", size=64, required=False, translate=False
    )
    z_receivable_export = fields.Char("Receivable Export", size=64, required=False)
    z_payable_export = fields.Char("Payable Export", size=64, required=False)
    purchase_default_account_id = fields.Many2one(
        "account.account",
        string="Purchase Default Account",
        required=False,
        help="Satın alma işlemlerinde varsayılan muhasebe hesabı.",
    )
    accounting_contact = fields.Many2one(
        "res.partner", string="Accounting Contact", required=False
    )
    devir_yapildi = fields.Boolean("Devir Yapıldı", default=False)
    due_days = fields.Integer(
        "Due Days",
        compute="_compute_due_days",
        store=False,
        default=0,
        search="_search_due_days",
    )

    @api.model
    def _compute_due_days(self):
        for record in self:
            if record.property_payment_term_id:
                record.due_days = max(
                    record.property_payment_term_id.line_ids.mapped("days") or [0],
                )

    @api.model
    def create(self, vals):
        if not vals.get("ref") and self._needsRef(vals=vals):
            vals["ref"] = self._get_next_ref(vals=vals)
            if (
                vals.get("ref")
                and vals.get("country_id")
                and vals.get("customer")
                or vals.get("supplier")
            ):
                country_id = self.env["res.country"].browse(vals["country_id"])
                if country_id and country_id.code != "TR":
                    z_receivable_export = "120.Y%s" % (vals["ref"].strip() or "")
                    z_payable_export = "320.Y%s" % (vals["ref"].strip() or "")
                else:
                    z_receivable_export = "120.%s" % (vals["ref"].strip() or "")
                    z_payable_export = "320.%s" % (vals["ref"].strip() or "")
                vals.update(
                    {
                        "ref": vals["ref"],
                        "z_receivable_export": z_receivable_export,
                        "z_payable_export": z_payable_export,
                    }
                )
        return super(ResPartner, self).create(vals)
