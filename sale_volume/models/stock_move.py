# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class StockMove(models.Model):

    _inherit = 'stock.move'

    product_uom_unit = fields.Integer(
        'units', compute='_compute_product_uom_unit',
        inverse='_inverse_product_uom_unit')
    initial_demand_units = fields.Integer(readonly=True)
    escuadria = fields.Char('Escuadría', readonly=True)
    escuadria_float = fields.Float(compute='_compute_escuadria_float',
                                   store=True)
    product_length = fields.Float(readonly=True)
    ud_qty_ratio = fields.Float(compute='_compute_ud_qty_ratio')

    @api.depends('initial_demand_units', 'product_uom_qty')
    def _compute_ud_qty_ratio(self):
        for move in self:
            move.ud_qty_ratio = self.product_uom_qty / self.initial_demand_units

    @api.depends('escuadria')
    def _compute_escuadria_float(self):
        for move_line in self.filtered(lambda r: r.escuadria):
            escuadria = move_line.escuadria.replace(',', '.').lower().replace(
                'x', '*')
            try:
                move_line.escuadria_float = safe_eval(escuadria)
            except ValueError:
                raise UserError(_('invalid escuadría'))

    @api.depends('move_line_ids.product_uom_unit')
    def _compute_product_uom_unit(self):
        for move in self:
            move.product_uom_unit = sum([x.product_uom_unit
                                         for x in move._get_move_lines()])

    def _inverse_product_uom_unit(self):
        for move in self:
            move_lines = move._get_move_lines()
            if not move_lines:
                move_line = self.env['stock.move.line'].create(
                    dict(move._prepare_move_line_vals(),
                         qty_done=move.quantity_done,
                         product_uom_unit=move.product_uom_unit))
                move.write({'move_line_ids': [(4, move_line.id)]})
            elif len(move_lines) == 1:
                move_lines[0].product_uom_unit = move.product_uom_unit
            else:
                raise UserError(_("Cannot set the done quantity from this "
                                  "stock move, work directly with the move"
                                  " lines."))
