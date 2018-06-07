# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class ProcurementRule(models.Model):

    _inherit = 'procurement.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_id, name, origin, values, group_id):
        res = super(ProcurementRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin,
            values, group_id)
        res['product_uom_unit'] = values.get('product_uom_unit', False)
        res['escuadria'] = values.get('escuadria', False)
        res['product_length'] = values.get('product_length', False)
        res['initial_demand_units'] = self._context.get('new_units', values.get('initial_demand_units', False))
        return res
