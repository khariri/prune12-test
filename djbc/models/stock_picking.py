from odoo import models, fields

class DJBCStockPicking(models.Model):
    _inherit='stock.picking'

    docs_id = fields.Many2one(string='DJBC Document',comodel_name='djbc.docs',)
