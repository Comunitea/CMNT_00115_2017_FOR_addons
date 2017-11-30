# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    product_uom_unit = fields.Float('units')
    escuadria = fields.Char('Escuadría', related='move_id.escuadria',
                            readonly=True)
    escuadria_float = fields.Float(
        'escuadría', related='move_id.escuadria_float', readonly=True)
    product_length = fields.Float(related='move_id.product_length',
                                  readonly=True)
    qty_done = fields.Float(compute='_compute_qty_done',
                            store=True)

    @api.depends('product_uom_unit', 'escuadria_float', 'product_length')
    def _compute_qty_done(self):
        for move_line in self:
            if not move_line.escuadria_float and not move_line.product_length:
                move_line.qty_done = move_line.product_uom_unit
            elif not move_line.escuadria_float and move_line.product_length:
                move_line.qty_done = move_line.product_uom_unit * \
                    move_line.product_length
            else:
                move_line.qty_done = move_line.product_uom_unit * \
                    move_line.escuadria_float / 10000 * \
                    move_line.product_length
