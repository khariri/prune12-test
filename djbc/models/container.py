from odoo import models, fields

class DJBCContainers(models.Model):
    _name='djbc.containers'
    _description='DJBC Containers'
    _rec_name='name'

    name = fields.Char(string='Container No', required=True,)
    container_size = fields.Char(string='Size', required=False,)
    container_type = fields.Char(string='Type', required=False,)
    gate_pass = fields.Char(string='Gate Pass', required=False,)
    doc_id = fields.Many2one(comodel_name="djbc.docs", string="DJBC Doc", required=False, )

