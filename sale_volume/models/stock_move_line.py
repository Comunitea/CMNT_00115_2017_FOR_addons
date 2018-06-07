# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class StockMoveLine(models.Model):

    _inherit = 'stock.move.line'

    product_uom_unit = fields.Integer('units')
    escuadria = fields.Char('Escuadría', related='move_id.escuadria',
                            readonly=True)
    escuadria_float = fields.Float(
        'escuadría', related='move_id.escuadria_float', readonly=True)
    product_length = fields.Float(related='move_id.product_length',
                                  readonly=True)
    qty_done = fields.Float(compute='_compute_qty_done',
                            inverse='_quantity_done_set', store=True)
    ud_qty_ratio = fields.Float(related='move_id.ud_qty_ratio',
                                readonly=True)
    qty_manual_done = fields.Float()

    def _quantity_done_set(self):
        """
            Solo se edita si unidades es 0
        """
        for line in self:
            line.qty_manual_done = line.qty_done

    @api.depends('product_uom_unit', 'escuadria_float', 'product_length',
                 'qty_manual_done')
    def _compute_qty_done(self):
        for move_line in self:
            move_line.qty_done = move_line.move_id.product_uom_unit * move_line.ud_qty_ratio
