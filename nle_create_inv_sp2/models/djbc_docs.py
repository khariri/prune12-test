from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)

class DJBCDocsInherit(models.Model):
    _inherit='djbc.docs'
    invoice_id = fields.Many2one(comodel_name="account.invoice", string="Invoice SP2", required=False, )





