# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from collections import OrderedDict
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_published = fields.Boolean(
        string="Is Published",
        help="If checked, the product will be published on the website.",
        default=False,
    )

    public_description = fields.Html(
        "Description for e-Commerce",
        sanitize_attributes=False,
        translate=False,
        copy=False,
    )

    website_attachment_ids = fields.Many2many(
        string="Website attachments",
        comodel_name="ir.attachment",
        help="Files publicly downloadable from the product eCommerce page.",
    )

    feature_line_ids = fields.One2many(
        comodel_name="product.template.feature.line",
        inverse_name="product_tmpl_id",
        string="Features",
    )

    def _prepare_product_attachments_table(self):
        """This method returns product attachments."""
        attachments = self.sudo().website_attachment_ids
        return attachments

    # def price_compute(
    #     self, price_type, uom=None, currency=None, company=None, date=False
    # ):
    #     """Override price_compute method to use sale_price field."""
    #     res = super(ProductTemplate, self).price_compute(
    #         "sale_price", uom=uom, currency=currency, company=company, date=date
    #     )
    #     return res
    # NOTE: price field is missing. You need to add sale_price to template

    @api.depends("attribute_line_ids.value_ids")
    def _compute_valid_product_template_attribute_line_ids(self):
        """Inherited to remove non-visible attributes from the combination."""
        res = super(
            ProductTemplate, self
        )._compute_valid_product_template_attribute_line_ids()
        for record in self:
            lines = record.valid_product_template_attribute_line_ids
            record.valid_product_template_attribute_line_ids = lines.filtered(
                lambda x: x.attribute_id.visibility != "hidden"
            )
        return res

    def _is_combination_possible(
        self, combination, parent_combination=None, ignore_no_variant=False
    ):
        """Inherited to remove non-visible attributes from the combination."""
        self.ensure_one()
        return super(ProductTemplate, self)._is_combination_possible(
            combination.filtered(lambda x: x.attribute_id.visibility != "hidden"),
            parent_combination=parent_combination,
            ignore_no_variant=ignore_no_variant,
        )

    def _prepare_categories_with_features(self, categories):
        """
        This method adds feature lines to the product specifications.
        If there are no ptal, it will create an empty list.
        param categories: OrderedDict of attributes and their values
        """
        ptal = categories.get(self.env["product.attribute.category"], False)
        #  Attributes first
        categories = OrderedDict({self.env["product.attribute.category"]: []})
        if ptal:
            for line in ptal.filtered(lambda x: len(x.value_ids) > 0):
                categories[self.env["product.attribute.category"]].append(line)

        ptfl = self.sudo().feature_line_ids
        for line in ptfl.filtered(lambda x: len(x.value_ids) > 0):
            categories[self.env["product.attribute.category"]].append(line)

        return categories


class ProductTemplateAttributeLine(models.Model):
    _inherit = "product.template.attribute.line"

    default_value_id = fields.Many2one(
        string="Default Value",
        comodel_name="product.attribute.value",
        help="Default value for the attribute.",
    )

    allow_filling = fields.Boolean(
        string="Allow Filling",
        help="If checked, attribute values will be filled automatically",
        related="attribute_id.allow_filling",
        readonly=True,
    )
