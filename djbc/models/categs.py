from odoo import models, fields

class DJBCCategs(models.Model):
    _name='djbc.categs'
    _description='DJBC Categories'
    _rec_name='name'

    name = fields.Text(string='DJBC Category', required=True,)
