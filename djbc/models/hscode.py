from odoo import models, fields

class DJBCHSCode(models.Model):
    _name='djbc.hscode'
    _description='DJBC HS Code'
    _rec_name='code'

    code = fields.Char(string='HS Code', required=True,)
    name = fields.Text(string='HS Description', required=True,)