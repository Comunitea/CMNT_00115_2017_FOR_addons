# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrderLineAddAttributes(models.TransientModel):
    _name = 'sale.order.line.add.attributes'

    attribute_list = fields.Many2many('sale.line.attribute')
    order_lines = fields.Many2many('sale.order.line')
    order_id = fields.Many2one('sale.order', default=lambda r: r.env.context.get('active_id', False))

    def set_attributes(self):
        for line in self.order_lines:
            line.write({'attribute_ids': [(4, x.id) for x in self.attribute_list]})
            line.with_context(from_wiz=True).update_attributes_price()
