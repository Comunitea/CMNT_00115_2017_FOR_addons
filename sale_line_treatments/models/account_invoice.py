# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    attribute_ids = fields.Many2many('sale.line.attribute',
                                     string='Attributes')
