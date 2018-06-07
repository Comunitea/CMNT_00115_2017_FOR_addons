# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'automatic volume in sale order lines quantity',
    'summary': '',
    'version': '11.0.1.0.0',
    'category': 'Sale',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'sale',
        'sale_stock'
    ],
    'data': [
        'views/sale_order_line_view.xml',
        'views/sale_line_attribute_view.xml',
        'views/stock_move_view.xml',
        'views/account_invoice.xml'
    ],
}
