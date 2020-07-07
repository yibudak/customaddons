# -*- coding: utf-8 -*-
#
#Created on Oct 12, 2018
#
#@author: dogan
#

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class CreateProcurementMove(models.TransientModel):
    _name = 'create.procurement.move'
        
    move_id = fields.Many2one('stock.move','Move', readonly=True)
    product_id = fields.Many2one('product.product',string='Product', related='move_id.product_id', readonly=True)
    
    move_qty = fields.Float('Demand Quantity', related='move_id.product_uom_qty', readonly=True)
    procure_move  = fields.Boolean('Harekete Tedarik Oluştur',default=True)
    qty_to_sincan = fields.Float('Quantity to Sincan Depo')
    qty_to_merkez = fields.Float('Quantity to Merkez Depo')
    qty_available_merkez = fields.Float('Merkez Depo Mevcut', related='product_id.qty_available_merkez')
    qty_available_sincan = fields.Float('Sincan Depo Mevcut', related='product_id.qty_available_sincan')
    qty_incoming_merkez = fields.Float('Merkez Depo Gelen', related='product_id.qty_incoming_merkez')
    qty_incoming_sincan = fields.Float('Sincan Depo Gelen', related='product_id.qty_incoming_sincan')
    qty_outgoing_merkez = fields.Float('Merkez Depo Giden', related='product_id.qty_outgoing_merkez')
    qty_outgoing_sincan = fields.Float('Sincan Depo Giden', related='product_id.qty_outgoing_sincan')
    qty_virtual_merkez = fields.Float('Merkez Depo Tahmini', related='product_id.qty_virtual_merkez')
    qty_virtual_sincan = fields.Float('Sincan Depo Tahmini', related='product_id.qty_virtual_sincan')
    uom = fields.Many2one('uom.uom', string='UoM', related='move_id.product_uom', readonly=True)
    
    production_ids = fields.Many2many('mrp.production',string='Manufacturing Orders', compute='_compute_productions')
    transfers_to_customer_ids = fields.Many2many('stock.move',string='Transfers to Customers',
                                                 compute='_compute_customer_transfers')
    pending_orderline_ids = fields.Many2many('sale.order.line', string='Pending Orders',
                                             compute='_compute_pending_orderlines')

    # sale_qty30days = fields.Float(u'Son 1 ayda satılan', related='move_id.product_id.sale_qty30days', readonly=True, store=False)
    # sale_qty180days = fields.Float(u'Son 6 ayda satılan', related='move_id.product_id.sale_qty180days', readonly=True, store=False)
    # sale_qty360days = fields.Float(u'Son 1 senede satılan', related='move_id.product_id.sale_qty360days', readonly=True, store=False)

    @api.multi
    @api.depends('product_id')
    def _compute_productions(self):
        for wizard in self:
            wizard.production_ids = self.env['mrp.production'].search([('product_id','=',wizard.product_id.id),('state','not in', ['done','cancel'])],limit=40,order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_customer_transfers(self):
        for wizard in self:
            wizard.transfers_to_customer_ids = self.env['stock.move'].search([('product_id','=',wizard.product_id.id),('state','not in', ['draft','done','cancel'])],limit=40,order='create_date desc')

    @api.multi
    @api.depends('product_id')
    def _compute_pending_orderlines(self):
        for wizard in self:
            wizard.pending_orderline_ids = self.env['sale.order.line'].search([('product_id','=',wizard.product_id.id),('state','not in', ['draft','done','cancel'])],limit=40,order='create_date desc')


    @api.onchange('move_id')
    def onchange_move_id(self):
        self.qty = self.move_id.remaining_qty
        
    
    @api.multi
    def action_create(self):
        self.ensure_one()

        if self.procure_move:
            self.move_id._do_unreserve()
            self.move_id.procure_method = 'make_to_order'
            self.move_id._action_confirm()

        if self.qty_to_sincan > 0.0:
            wh = self.env['stock.warehouse'].browse([2])
            group_id = self.env("procurement.group").create({
                'name': u"Sincana Açan: " + self.env.user.name,
            })
            values = {
                'company_id': wh.company_id,
                'date_planned': self.move_id.date_expected,
                'move_dest_ids': self.move_id,
                'group_id': group_id,
                'route_ids': self.route_ids,
                'warehouse_id': wh,
            }
            product_qty = self.qty_to_sincan
            product_uom = self.uom
            product = self.product_id
            location = wh.lot_stock_id
            origin = (self.move_id.picking_id.name or "/")

            self.env['procurement.group'].run(product, product_qty, product_uom, location, "/", origin, values)

        if self.qty_to_merkez > 0.0:
            wh = self.env['stock.warehouse'].browse([1])
            group_id = self.env("procurement.group").create({
                'name': u"Merkeze Açan: " + self.env.user.name,
            })
            values = {
                'company_id': wh.company_id,
                'date_planned': self.move_id.date_expected,
                'move_dest_ids':  self.move_id,
                'group_id': group_id,
                'route_ids': self.move_id.route_ids,
                'warehouse_id': wh,
            }
            product_qty = self.qty_to_merkez
            product_uom = self.uom
            product = self.product_id
            location = wh.lot_stock_id
            origin = (self.move_id.picking_id.name or "/")

            self.env['procurement.group'].run(product, product_qty, product_uom.id, location, "/", origin, values)

        return {}


