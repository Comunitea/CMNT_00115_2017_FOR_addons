# © 2018 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Sale order line attributes',
    'version': '10.0.1.0.0',
    'summary': 'Add attributes on sale lines an update prices',
    'category': 'Sale',
    'depends': [
        'sale',
        'sale_volume'
    ],
    'data': [
        'views/sale_line_attribute.xml',
        'wizard/sale_order_line_add_attributes.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}
