# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    product_uom_unit = fields.Float('units')
    escuadria = fields.Char('Escuadría')
    escuadria_float = fields.Float(compute='_compute_escuadria_float',
                                   store=True)
    product_length = fields.Float()
    quantity = fields.Float('')
    quantity = fields.Float(compute='_compute_quantity',
                            store=True)

    @api.model
    def create(self, vals):
        '''
            Cuando se crea una linea con una cantidad hacemos el calculo de las
            unidades
        '''
        line = super(AccountInvoiceLine, self).create(vals)
        if vals.get('quantity', False):
            if not line.escuadria_float and not line.product_length:
                line.product_uom_unit = vals.get('quantity')
            elif not line.escuadria_float and line.product_length:
                line.product_uom_unit = vals.get('quantity') \
                    / line.product_length
            else:
                line.product_uom_unit = vals.get('quantity') / \
                    line.escuadria_float * 10000 / line.product_length
        return line

    @api.multi
    def write(self, vals):
        return super(AccountInvoiceLine, self).write(vals)

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
    def _compute_quantity(self):
        for line in self:
            if not line.escuadria_float and not line.product_length:
                line.quantity = line.product_uom_unit
            elif not line.escuadria_float and line.product_length:
                line.quantity = line.product_uom_unit * \
                    line.product_length
            else:
                line.quantity = line.product_uom_unit * \
                    line.escuadria_float / 10000 * line.product_length
