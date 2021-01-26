from odoo import fields, models
from odoo.addons import decimal_precision as dp


class ResCurrency(models.Model):
    _inherit = "res.currency"

    rate = fields.Float(digits=dp.get_precision('Currency Precision'))
    rounding = fields.Float(digits=dp.get_precision('Currency Precision'))


class ResCurrencyRate(models.Model):
    _inherit = "res.currency.rate"

    rate = fields.Float(digits=dp.get_precision('Currency Precision'))
