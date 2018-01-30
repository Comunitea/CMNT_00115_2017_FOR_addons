# -*- coding: utf-8 -*-
# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Custom documents',
    'summary': 'Antes de instalar poner como actualizable external_id base.paperformat_euro',
    'version': '8.0.1.0.0',
    'category': 'Uncategorized',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'account_payment_sale',
        'stock'
    ],
    'data': [
        'views/ir_qweb.xml',
        'views/report_sale_order.xml',
        'views/report_deliveryslip.xml',
        'views/report_invoice.xml',
        'data/report_paperformat.xml'
    ],
}
