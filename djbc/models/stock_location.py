from odoo import models, fields

class DJBCStockLocation(models.Model):
    _inherit='stock.location'

    is_stock_location = fields.Boolean(string="Is a Stock Location?",  )
