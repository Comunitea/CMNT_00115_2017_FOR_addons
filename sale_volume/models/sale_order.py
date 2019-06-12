# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    forewarned = fields.Boolean('Forewarned', default=False)
    done = fields.Boolean('Done', default=False)
