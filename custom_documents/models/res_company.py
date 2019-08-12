# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    picking_note = fields.Text(
        string='Default Terms and Conditions', translate=True)
