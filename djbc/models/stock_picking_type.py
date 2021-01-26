from odoo import models, fields

class DJBCStockPickingType(models.Model):
    _inherit='stock.picking.type'

    move_type = fields.Selection([('in','in'),('out','out'),],string='Move Type', required=False,)
