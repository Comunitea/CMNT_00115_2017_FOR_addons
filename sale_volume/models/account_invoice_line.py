# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    product_uom_unit = fields.Integer('units')
    escuadria = fields.Char('Escuadría')
    escuadria_float = fields.Float(compute='_compute_escuadria_float',
                                   store=True)
    product_length = fields.Float()
    quantity = fields.Float('')
    ud_qty_ratio = fields.Float(default=1)

    @api.model
    def create(self, vals):
        '''
            Cuando se crea una linea con una cantidad hacemos el calculo de las
            unidades. Si viene de un pedido de venta simplemente usaremos
            el ud_qty_ratio.
        '''
        line = super().create(vals)
        if self._context.get('from_so', False):
            if vals.get('ud_qty_ratio') == 0 or not vals.get(
                    'ud_qty_ratio', False):
                line.product_uom_unit = 0
            else:
                line.product_uom_unit = round(
                    vals.get('quantity') / vals.get('ud_qty_ratio'))
        return line

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
    def _compute_quantity(self):
        for line in self:
            if not line.escuadria_float and not line.product_length:
                line.quantity = line.product_uom_unit * line.ud_qty_ratio
            elif not line.escuadria_float and line.product_length:
                line.quantity = line.product_uom_unit * \
                    line.product_length
            elif not line.product_length:
                # Puede haber casos en los que se establezca
                # escuadria pero no longitud
                pass
            else:
                if line.escuadria.find('x') != -1 or line.escuadria.find(
                        'X') != -1:
                    line.quantity = line.product_uom_unit * \
                                           line.escuadria_float / 10000 * \
                                           line.product_length
                else:
                    line.quantity = line.product_uom_unit * \
                                           line.escuadria_float / 100 * \
                                           line.product_length
