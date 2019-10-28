# © 2019 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import datetime, timedelta

from odoo import fields, models


class SituationReport(models.TransientModel):

    _name = "situation.report"

    include_orders = fields.Boolean(default=True)
    include_bank_movements = fields.Boolean(default=True)
    include_customer_invoices = fields.Boolean(default=True)
    include_supplier_invoices = fields.Boolean(default=True)
    include_pagares = fields.Boolean(default=True)
    bank_movements_weeks = fields.Integer("Weeks")
    customer_invoices_weeks = fields.Integer("Weeks")
    supplier_invoices_weeks = fields.Integer("Weeks")

    sale_order_ids = fields.Many2many("sale.order")
    customer_invoices = fields.Many2many(
        "account.invoice", "situation_customer_invoices"
    )
    supplier_invoices = fields.Many2many(
        "account.invoice", "situation_supplier_invoices"
    )
    pagares_rec = fields.Many2many("account.move.line", "pagares_move_line1")
    pagares_ent = fields.Many2many("account.move.line", "pagares_move_line2")

    @staticmethod
    def get_start_date(weeks):
        start = (
            datetime.now()
            + timedelta(weeks=-weeks)
            + timedelta(days=-datetime.now().weekday())
        )
        return start.date()

    def generate_report(self):
        self.ensure_one()
        if self.include_orders:
            self.sale_order_ids = (
                self.env["sale.order"]
                .sudo()
                .search(
                    [
                        ("state", "in", ("sale", "done")),
                        ("invoice_status", "!=", "invoiced"),
                        ("confirmation_date", ">", "2019-10-20"),
                    ]
                )
            )
        if self.include_customer_invoices:
            customer_invoices_date = self.get_start_date(
                self.customer_invoices_weeks
            )
            self.customer_invoices = (
                self.env["account.invoice"]
                .sudo()
                .search(
                    [
                        ("state", "in", ("open", "paid")),
                        ("date_invoice", ">=", customer_invoices_date),
                        ("type", "=", "out_invoice"),
                    ]
                )
            )
        if self.include_supplier_invoices:
            supplier_invoices_date = self.get_start_date(
                self.supplier_invoices_weeks
            )
            self.supplier_invoices = (
                self.env["account.invoice"]
                .sudo()
                .search(
                    [
                        ("state", "in", ("open", "paid")),
                        ("date_invoice", ">=", supplier_invoices_date),
                        ("type", "=", "in_invoice"),
                    ],
                    order="date_invoice desc",
                )
            )
        if self.include_pagares:
            account_group = self.env.ref("l10n_es.account_group_431")
            self.pagares_rec = self.env["account.move.line"].search(
                [
                    ("reconciled", "=", False),
                    ("account_id.group_id", "=", account_group.id),
                    ("debit", ">", 0),
                ]
            )
            account_group = self.env.ref("l10n_es.account_group_401")
            self.pagares_ent = self.env["account.move.line"].search(
                [
                    ("reconciled", "=", False),
                    ("account_id.group_id", "=", account_group.id),
                    ("credit", ">", 0),
                ]
            )
        return self.env.ref(
            "situation_report.action_situation_report"
        ).report_action(self)

    def get_bank_datas(self):
        return_data = {"cash": {}}
        bank_movements_date = self.get_start_date(self.bank_movements_weeks)
        bank_statement_ids = (
            self.env["account.bank.statement.line"]
            .sudo()
            .search([("date", ">=", bank_movements_date)])
        )
        for statement in bank_statement_ids.sorted(
            key=lambda r: r.date, reverse=True
        ):
            if statement.statement_id.journal_id.type == "cash":
                if statement.company_id not in return_data["cash"]:
                    return_data["cash"][statement.company_id] = self.env[
                        "account.bank.statement.line"
                    ]
                return_data["cash"][statement.company_id] += statement
            else:
                if statement.company_id not in return_data:
                    return_data[statement.company_id] = {}
                if (
                    statement.statement_id.journal_id
                    not in return_data[statement.company_id]
                ):
                    return_data[statement.company_id][
                        statement.statement_id.journal_id
                    ] = self.env["account.bank.statement.line"]
                return_data[statement.company_id][
                    statement.statement_id.journal_id
                ] += statement
        return return_data
