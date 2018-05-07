# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class ProductProduct(models.Model):

    _inherit = 'product.product'




    @api.one
    def _compute_partner_ref(self):
        super(ProductProduct, self)._compute_partner_ref()
        for supplier_info in self.seller_ids:
            if supplier_info.name.id == self._context.get('partner_id'):
                product_name = supplier_info.product_name or self.default_code
        else:
            product_name = self.name
        code = self._context.get('display_default_code', True) and self.code or False
        self.partner_ref = '%s%s' % (code and '[%s] ' % code or '', product_name)
