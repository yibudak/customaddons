# -*- coding: utf-8 -*-
{
    'name': "Altinkaya Excel Reports",
    'summary': """
        Various Excel reports""",
    'description': """
        This module will allow exporting in Excel using
        OCA/server-tools/excel_import_export module.
    """,
    'author': "Yavuz Avcı,Yiğit Budak",
    'website': "",
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['excel_import_export', 'purchase', 'account'],
    'data': [
        # Purchase
        'export_purchase_order_xlsx/reports.xml',
        'export_purchase_order_xlsx/temp_po_en.xml',
        'export_purchase_order_xlsx/temp_po_tr.xml',
        'export_purchase_order_xlsx/temp_rfq_en.xml',
        'export_purchase_order_xlsx/temp_rfq_tr.xml',
        # Account
        'export_account_invoice_xlsx/temp_zirve_masraf_fatura.xml',
        'export_account_invoice_xlsx/temp_gelir_fatura.xml',
        'export_account_invoice_xlsx/reports.xml',
        # Partner Statement
        'export_partner_statement/temp_partner_statement.xml',
        'export_partner_statement/reports.xml',
        # Partner Statement Currency
        'export_partner_currency_statement/temp_partner_statement_currency.xml',
        'export_partner_currency_statement/reports.xml',
        # Payment Excel
        'export_account_payment_xlsx/reports.xml',
        'export_account_payment_xlsx/temp_payments.xml',
        # Move Line Excel
        'export_account_move_line_xlsx/reports.xml',
        'export_account_move_line_xlsx/temp_move_lines.xml',
        # Kviks Excel
        'export_account_invoice_kviks_xlsx/reports.xml',
        'export_account_invoice_kviks_xlsx/temp_kviks.xml',
    ],
    'installable': True,
}
