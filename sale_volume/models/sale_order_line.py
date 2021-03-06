# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_uom_unit = fields.Float('units')
    escuadria = fields.Char('Escuadría')
    escuadria_float = fields.Float(
        compute='_compute_escuadria_float', store=True)
    product_length = fields.Float()
    ud_delivered = fields.Float(copy=False)

    def name_get(self):
        result = []
        for so_line in self:
            name = '%s %s - %s - %s' % (
                so_line.product_uom_unit, so_line.name.split('\n')[0] or
                so_line.product_id.name, so_line.escuadria,
                so_line.product_length)
            result.append((so_line.id, name))
        return result

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
                # Puede haber casos en los que se establezca
                # escuadria pero no longitud
                pass
            else:
                if line.product_uom.category_id == \
                            self.env.ref('product.uom_categ_length') and \
                            line.product_length:
                    line.product_uom_qty = line.product_uom_unit * \
                        line.product_length
                elif line.product_uom.category_id == \
                        self.env.ref('product.product_uom_categ_unit'):
                    line.product_uom_qty = line.product_uom_unit
                else:
                    if line.escuadria.find('x') != -1 or line.escuadria.find(
                            'X') != -1:
                        line.product_uom_qty = line.product_uom_unit * \
                            line.escuadria_float / 10000 * line.product_length
                    else:
                        line.product_uom_qty = line.product_uom_unit * \
                            line.escuadria_float / 100 * line.product_length

    def _prepare_procurement_values(self, group_id=False):
        res = super()._prepare_procurement_values(group_id)
        res['escuadria'] = self.escuadria
        res['product_length'] = self.product_length
        res['initial_demand_units'] = self.product_uom_unit
        return res

    @api.multi
    def invoice_line_create(self, invoice_id, qty):
        return super(
            SaleOrderLine,
            self.with_context(from_so=True)).invoice_line_create(
                invoice_id, qty)

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super()._prepare_invoice_line(qty)
        if self.product_uom_unit == 0:
            res['ud_qty_ratio'] = 0
        else:
            res['ud_qty_ratio'] = self.product_uom_qty / self.product_uom_unit
        res['escuadria'] = self.escuadria
        res['product_length'] = self.product_length
        return res

    @api.multi
    def _action_launch_procurement_rule(self):
        """
        Pasamos la cantidad en unidades que tendrá el nuevo movimiento
        """
        for line in self:
            if line.state != 'sale' or line.product_id.type not in \
                    ('consu', 'product'):
                continue
            qty = 0.0
            for move in line.move_ids.filtered(lambda r: r.state != 'cancel'):
                qty += move.initial_demand_units
            new_units = line.product_uom_unit - qty
            # Cuando se confirma el pedido se llama con todas las lineas,
            # por lo que llamamos a super por cada linea.
            super(
                SaleOrderLine,
                line.with_context(new_units=new_units))._action_launch_procurement_rule()
        return True

    @api.multi
    def _get_delivered_ud(self):
        self.ensure_one()
        qty = 0.0
        for move in self.move_ids.filtered(
                lambda r: r.state == 'done' and not r.scrapped):
            if move.location_dest_id.usage == "customer":
                if not move.origin_returned_move_id:
                    qty += move.product_uom_unit
            elif move.location_dest_id.usage != "customer" and move.to_refund:
                qty -= move.product_uom_unit
        return qty
