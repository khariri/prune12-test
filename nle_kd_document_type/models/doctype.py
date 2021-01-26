from odoo import models, fields

class DJBCDocType(models.Model):
    _inherit='djbc.doctype'

    kd_document_type = fields.Char(string='Kode Document Type (SP2)', required=False,)
