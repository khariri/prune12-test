from odoo import models, fields

class DJBCStockMove(models.Model):
    _inherit='stock.move'
    djbc_masuk_flag = fields.Boolean(string='DJBC Masuk')
    djbc_keluar = fields.Boolean(string='DJBC Keluar')
    sisa_qty = fields.Float(string='Sisa Qty')
    jumlah_kemasan = fields.Float(string="Jumlah Kemasan", required=False, )
    satuan_kemasan = fields.Char(string="Satuan Kemasan", required=False, )
