# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Partner financial risk",
    "version": "12.0.1.0.0",
    "category": "Sales Management",
    "website": "https://nodrizatech.com/",
    "author": "Odoo Nodriza Tech (ONT), "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "base",
        "account",
        "sale",
        "crm",
        "account_payment_mode",  # https://github.com/OCA/bank-payment
        "account_payment_partner",  # https://github.com/OCA/bank-payment
        "account_payment_sale"  # https://github.com/OCA/bank-payment
    ],
    "data": [
        "views/account_payment_mode_view.xml",
        "views/crm_lead_view.xml",
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
    "installable": True
}
