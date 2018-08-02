# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
from odoo.tools.misc import formatLang


class AccountJournal(models.Model):

    _inherit = 'account.journal'

    @api.multi
    def get_journal_dashboard_datas(self):
        currency = self.currency_id or self.company_id.currency_id
        res = super(AccountJournal, self).get_journal_dashboard_datas()
        journals = self.env['account.journal'].sudo().search(
            [('type', '=', 'cash')])
        total_last_balance = 0.0
        for journal in journals:
            last_bank_stmt = self.env['account.bank.statement'].sudo().search(
                [('journal_id', '=', journal.id)],
                order="date desc, id desc", limit=1)
            total_last_balance += last_bank_stmt and \
                last_bank_stmt[0].balance_end or 0
        res['total_last_balance'] = formatLang(
            self.env,
            currency.round(total_last_balance) + 0.0, currency_obj=currency)
        return res
