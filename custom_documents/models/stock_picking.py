# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, exceptions, _


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.model
    def create(self, vals):
        if vals.get('company_id', False) and not vals.get('note', False):
            vals['note'] = self.env['res.company'].browse(vals['company_id']).picking_note
        return super(StockPicking,self).create(vals)
