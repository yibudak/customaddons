from odoo import api, fields, models, tools, _
from datetime import datetime

class ResCurrency(models.Model):
    _inherit = 'res.currency'


    def convert_currency_rate(self, from_amount, to_currency, company, date):
        to_currency_id = self.env['res.currency'].browse(to_currency)
        company_id = self.env['res.company'].browse(company)
        return [to_currency_id.symbol, self._convert(from_amount, to_currency_id, company_id, datetime.strptime(date, '%d-%m-%Y'), True)]
