# -*- coding: utf-8 -*-


from openerp.osv import osv, fields
from openerp.tools.translate import _
import math

class account_invoice(osv.osv):
    _inherit = "account.invoice"
    _columns = {
        'packing_tracking_ids': fields.one2many('stock.tracking', 'invoice_id', 'Packing Details'),
    }

    def btn_calc_weight_inv(self, cr, uid, ids, context=None):
        total_g, total_n, total_p = 0, 0, 0
        total_vol = total_air = total_land = 0

        for pack in self.browse(cr, uid, ids[0], context).packing_tracking_ids:
                total_g += pack.gross_weight
                total_n += pack.net_weight
                total_p += 1
                total_vol += (((pack.pack_h * pack.pack_w * pack.pack_l) * 1.0) / 1000000)
                total_air += math.ceil(((pack.pack_h * pack.pack_h * pack.pack_h) * 1.0) / 5000)
                total_land += math.ceil(((pack.pack_h * pack.pack_h * pack.pack_h) * 1.0) / 3000)
        vals = {
           'total_grosswg': total_g,
           'total_netwg': total_n,
           'total_num_pack': total_p,
           'total_volume': total_vol,
           'total_air': total_air,
           'total_land': total_land,
        }
        self.write(cr, uid, ids, vals, context)
        return True

    def merge_invoice_lines(self, cr, uid, ids, context=None):
        invoice_line_obj = self.pool.get('account.invoice.line')
        cr.execute("select pp.id,ail.name,ail.account_id,sum(quantity),ail.uos_id,ail.price_unit,ail.discount,lt.tax_id\
                            from account_invoice_line ail\
                            left join product_product pp on (pp.id=ail.product_id)\
                            left join product_template pt on (pt.id=pp.product_tmpl_id)\
                            left join account_invoice_line_tax lt on (ail.id=lt.invoice_line_id)\
                            where invoice_id=%s\
                            group by pp.id,ail.name,ail.account_id,ail.uos_id,ail.price_unit,ail.discount,lt.tax_id"\
                            % ids[0])
        res = cr.fetchall()
        invoice = self.browse(cr, uid, ids[0], context=None)
        line_ids = map(lambda a: a.id, invoice.invoice_line)
        if line_ids:
            invoice_line_obj.unlink(cr, uid, line_ids, context=context)
        for line in res:
            vals = {
                 'product_id': line[0],
                 'name': line[1],
                 'account_id': line[2],
                 'quantity': line[3],
                 'uos_id': line[4],
                 'price_unit': line[5],
                 'discount': line[6],
                 'invoice_line_tax_id': [(6,0,[line[7]])],
                 'invoice_id': ids[0],
            }
            invoice_line_obj.create(cr, uid, vals)


account_invoice()