# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class SaleLineAttribute(models.Model):
    _name = "sale.line.attribute"

    name = fields.Char(required=True)
    unit_prices = fields.One2many('sale.line.attribute.price', 'attribute_id')

    @api.multi
    def get_price_unit(self, uom):
        if uom in self.mapped('unit_prices.uom_id'):
            return self.unit_prices.filtered(
                lambda r: r.uom_id == uom).price_unit
        same_categ_uom = self.unit_prices.filtered(
            lambda r: r.uom_id.category_id == uom.category_id)
        if not same_categ_uom:
            raise UserError(_('Price not configured for UoM %s') % uom.name)
        return same_categ_uom.uom_id._compute_price(
            same_categ_uom.price_unit, uom)


class SaleLineAttributePrice(models.Model):
    _name = 'sale.line.attribute.price'

    uom_id = fields.Many2one('product.uom', 'Unit of mesure', required=True)
    price_unit = fields.Float()
    attribute_id = fields.Many2one('sale.line.attribute')

    @api.constrains('uom_id')
    def check_not_repeated_uom(self):
        repeated_uom = self.attribute_id.unit_prices.filtered(
            lambda r: r.uom_id == self.uom_id and r.id != self.id)
        if repeated_uom:
            raise ValidationError(
                    _('UoM %s repeated for the attribute') % self.uom_id.name)

        repeated_category = self.attribute_id.unit_prices.filtered(
            lambda r: r.uom_id.category_id == self.uom_id.category_id and
            r.id != self.id)
        if repeated_category:
            raise ValidationError(
                    _('UoM category %s repeated for the attribute')
                    % self.uom_id.category_id.name)
