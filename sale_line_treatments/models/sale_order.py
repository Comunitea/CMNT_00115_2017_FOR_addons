# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    attribute_ids = fields.Many2many('sale.line.attribute',
                                     string='Attributes')
    attribute_prices = fields.One2many(
        'sale.order.line.attribute.price', 'line_id')

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super()._prepare_invoice_line(qty)
        res['attribute_ids'] = [(6, 0, self.attribute_ids.ids)]
        return res

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res = super().product_id_change()
        if self.product_id:
            self.set_att_name()
        else:
            self.attribute_ids = None
        return res

    @api.onchange('attribute_ids')
    def attribute_ids_change(self):
        if self.product_id:
            self.update_attributes_price()

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        res = super().product_uom_change()
        self.attribute_prices = [(2, x.id) for x in self.attribute_prices]
        self.update_attributes_price()
        return res

    def set_att_name(self):
        self.name = self.product_id.name
        attr_str = ""
        if self.attribute_ids:
            attr_str = " (" + ", ".join(
                self.attribute_ids.mapped('name')) + ")"
            self.name += attr_str

    def update_attributes_price(self):
        self.price_unit -= sum([x.price for x in self.attribute_prices])
        for attribute in self.attribute_ids:
            created_price = self.attribute_prices.filtered(
                lambda r: r.attribute_id.id == attribute.id)
            price = attribute.get_price_unit(self.product_uom)
            if not created_price:
                attribute_dict = {
                    'attribute_id': attribute.id,
                    'price': price,
                    'line_id': self.id}
                if self._context.get('from_wiz', False):
                    self.attribute_prices.create(attribute_dict)
                else:
                    self.attribute_prices.new(attribute_dict)
            else:
                if created_price.price != price:
                    created_price.price = price
        # Se ha elminado alguna etiqueta
        if self.mapped('attribute_prices.attribute_id') - self.attribute_ids:
            list_ = [(2, x.id) for x in self.attribute_prices.filtered(
                lambda r: r.attribute_id not in self.attribute_ids)]
            list_ += [(6, 0, [x.id for x in self.attribute_prices.filtered(
                     lambda r: r.attribute_id in self.attribute_ids)])]
            self.update({'attribute_prices': list_})
        new_price = sum(self.mapped('attribute_prices.price'))
        self.price_unit += new_price


class SaleOrderLineAttributePrice(models.Model):

    _name = 'sale.order.line.attribute.price'

    line_id = fields.Many2one('sale.order.line')
    price = fields.Float()
    attribute_id = fields.Many2one('sale.line.attribute')
