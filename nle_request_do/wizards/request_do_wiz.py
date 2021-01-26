import logging
from datetime import datetime
import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class RequestDOWizard(models.TransientModel):
    _name='request.do.wizard'

    shipping_name = fields.Many2one(comodel_name="res.partner", string="Shipping Name", required=False,
                               domain=[('nle_category', '=', 'shipping'), ])

    @api.multi
    def request_do(self):

        my_do = self.env['djbc.docs'].browse(self.env.context.get('active_id'))
        my_do.write({'shipping_name':self.shipping_name.id})
        my_do.write({'state':'req_do'})
        my_do.write({'status_do': 'Request'})
        my_do.write({'request_date': datetime.today()})

        # _logger.info('KEREN--->' + str(my_sp2.party))



