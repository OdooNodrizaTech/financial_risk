# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Partner financial risk',
    'version': '12.0.1.0.0',    
    'author': 'Odoo Nodriza Tech (ONT)',
    'website': 'https://nodrizatech.com/',
    'category': 'Tools',
    'license': 'AGPL-3',
    'depends': ['base', 'account', 'sale', 'crm'],
    'data': [
        'views/account_payment_mode_view.xml',
        'views/crm_lead_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'auto_install': False,    
}