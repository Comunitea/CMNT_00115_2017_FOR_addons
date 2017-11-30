# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    product_uom_unit = fields.Float('units')
    escuadria = fields.Char('Escuadría')
    escuadria_float = fields.Float(compute='_compute_escuadria_float',
                                   store=True)
    product_length = fields.Float()
    product_uom_qty = fields.Float(compute='_compute_product_uom_qty',
                                   store=True)

    @api.depends('escuadria')
    def _compute_escuadria_float(self):
        for line in self.filtered(lambda r: r.escuadria):
            escuadria = line.escuadria.replace(',', '.').lower().replace(
                'x', '*')
            try:
                line.escuadria_float = safe_eval(escuadria)
            except ValueError:
                raise UserError(_('invalid escuadría'))

    @api.depends('product_uom_unit', 'escuadria', 'product_length')
    def _compute_product_uom_qty(self):
        for line in self:
            if not line.escuadria_float and not line.product_length:
                line.product_uom_qty = line.product_uom_unit
            elif not line.escuadria_float and line.product_length:
                line.product_uom_qty = line.product_uom_unit * \
                    line.product_length
            else:
                line.product_uom_qty = line.product_uom_unit * \
                    line.escuadria_float / 10000 * line.product_length

    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        res['escuadria'] = self.escuadria
        res['product_length'] = self.product_length
        res['initial_demand_units'] = self.product_uom_unit
        return res
