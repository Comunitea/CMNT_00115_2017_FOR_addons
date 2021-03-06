# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountPaymentMode(models.Model):

    _inherit = 'account.payment.mode'

    def get_bank_strings(self):
        if not self:
            return []
        self.ensure_one()
        banks = []
        if self.bank_account_link == 'fixed' and \
                self.fixed_journal_id.bank_account_id:
            bank_account = self.fixed_journal_id.bank_account_id
            banks.append('{}: {}'.format(
                bank_account.bank_id.name,
                bank_account.acc_number))
        else:
            for journal in self.variable_journal_ids.filtered(
                    lambda r: r.bank_account_id):
                banks.append('{}: {}'.format(
                    journal.bank_account_id.bank_id.name,
                    journal.bank_account_id.acc_number))
        return banks
