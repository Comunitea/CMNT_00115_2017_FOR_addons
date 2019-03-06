# -*- coding: utf-8 -*

##############################################################################
#
#    License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
#    © 2019 Comunitea - Ruben Seijas <ruben@comunitea.com>
#    © 2019 Comunitea - Pavel Smirnov <pavel@comunitea.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.template'

    escuadria = fields.Char('Escuadría', compute="_compute_escuadria", store=True)
    height = fields.Integer('Alto', default="0")
    width = fields.Integer('Ancho', default="0")
    length = fields.Float('Largo')
    dimension = fields.Char('Dimensión', readonly=True, default="N/D", compute="_compute_escuadria", store=True)

    @api.depends('height', 'width', 'length')
    def _compute_escuadria(self):
        for record in self:
            if record.height and record.height != "0" \
                    and record.width and record.width != "0":
                record.escuadria = "%sx%s" % (str(record.height), str(record.width))
                record.dimension = record.escuadria
                if record.length and record.length != "0":
                    record.dimension += "x%s" % str(int(record.length))
