from odoo import models, fields

class DJBCProductTemplate(models.Model):
    _inherit='product.template'
    #djbc_category = fields.Selection(
    #    [('bb', 'Bahan Baku'),
    #     ('bj', 'Barang Jadi'),
    #     ('sc', 'Scrap/Reject'),
    #     ('ms', 'Mesin'),],
    #    string='DJBC Category',
    #    default='bb')
    hscode = fields.Many2one(comodel_name="djbc.hscode", string="HS Code", required=False, )
    djbc_category_id = fields.Many2one(comodel_name="djbc.categs", string="DJBC Category", required=False, )
