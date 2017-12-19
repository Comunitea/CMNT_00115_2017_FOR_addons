# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ResPartner(models.Model):

    _inherit = 'res.partner'

    cod_import_1 = fields.Char('Cuenta 1')
    cod_import_2 = fields.Char('Cuenta 2')
    cod_import_3 = fields.Char('Cuenta 3')

