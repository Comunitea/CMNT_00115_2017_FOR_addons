# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):
        for picking in self.pick_ids:
            for move in picking.move_lines:
                for move_line in move.move_line_ids:
                    move_line.product_uom_unit = move.initial_demand_units
        return super(StockImmediateTransfer, self).process()
