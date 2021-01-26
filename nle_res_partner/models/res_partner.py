from odoo import models, fields

class NLEResPartner(models.Model):
    _inherit='res.partner'

    nle_category = fields.Selection(
        string="NLE Category",
        selection=[
            ("consignee", "Cargo Owner"),
            ("ppjk", "FF/PPJK"),
            ("shipping", "Shipping Line"),
            ("terminal", "Terminal Operator"),
        ],
        required=False,
    )
