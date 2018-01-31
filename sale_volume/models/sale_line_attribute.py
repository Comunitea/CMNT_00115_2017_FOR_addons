# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class SaleLineAttribute(models.Model):
    _name = "sale.line.attribute"

    name = fields.Char('Name')
