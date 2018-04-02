# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, exceptions, _


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    @api.onchange('product_id')
    def _onchange_product_id2(self):
        return self.with_context(display_default_code=False)._onchange_product_id()
