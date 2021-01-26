from odoo import models, fields

class DJBCStockInventory(models.Model):
    _inherit='stock.inventory'
    djbc_mark=fields.Boolean(string='DJBC Marking')	
