# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    product_uom_unit = fields.Integer('units')
    escuadria = fields.Char('Escuadría')
    escuadria_float = fields.Float(compute='_compute_escuadria_float',
                                   store=True)
    product_length = fields.Float()
    attribute_ids = fields.Many2many(
        comodel_name='sale.line.attribute',
        string='Attributes',
    )

    @api.depends('escuadria')
    def _compute_escuadria_float(self):
        for line in self.filtered(lambda r: r.escuadria):
            escuadria = line.escuadria.replace(',', '.').lower().replace(
                'x', '*')
            try:
                line.escuadria_float = safe_eval(escuadria)
            except ValueError:
                raise UserError(_('invalid escuadría'))

    @api.onchange('product_uom_unit', 'escuadria', 'product_length')
    def _compute_product_uom_qty(self):
        for line in self:
            if not line.escuadria_float and not line.product_length:
                line.product_uom_qty = line.product_uom_unit
            elif not line.escuadria_float and line.product_length:
                line.product_uom_qty = line.product_uom_unit * \
                    line.product_length
            elif not line.product_length:
                # Puede haber casos en los que se establezca escuadria pero no longitud
                pass
            else:
                if line.escuadria.find('x') != -1 or line.escuadria.find(
                        'X') != -1:
                    line.product_uom_qty = line.product_uom_unit * \
                        line.escuadria_float / 10000 * line.product_length
                else:
                    line.product_uom_qty = line.product_uom_unit * \
                        line.escuadria_float / 100 * line.product_length

    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        res['escuadria'] = self.escuadria
        res['product_length'] = self.product_length
        res['initial_demand_units'] = self.product_uom_unit
        return res

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        if self.product_uom_unit == 0:
            res['ud_qty_ratio'] = 0
        else:
            res['ud_qty_ratio'] = self.product_uom_qty / self.product_uom_unit
        res['escuadria'] = self.escuadria
        res['product_length'] = self.product_length
        res['attribute_ids'] = [(6, 0, self.attribute_ids.ids)]
        return res

    @api.multi
    @api.onchange('product_id', 'attribute_ids')
    def product_id_change(self):
        res = super(SaleOrderLine, self).product_id_change()
        if self.product_id:
            self.name = self.product_id.name
            attr_str = ""
            if self.attribute_ids:
                attr_str = " (" + ", ".join(
                    self.attribute_ids.mapped('name')) + ")"
            self.name += attr_str
        else:
            self.attribute_ids = None

        return res
