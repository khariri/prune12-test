import logging
from datetime import datetime
import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class RequestSP2Wizard(models.TransientModel):
    _name='request.sp2.wizard'

    terminal = fields.Many2one(comodel_name="res.partner", string="Terminal", required=False,
                               domain=[('nle_category', '=', 'terminal'), ])

    @api.multi
    def request_sp2(self):

        my_sp2 = self.env['djbc.docs'].browse(self.env.context.get('active_id'))
        my_sp2.write({'terminal':self.terminal.id})
        my_sp2.write({'state':'req_sp2'})
        my_sp2.write({'status': 'Request'})
        my_sp2.write({'request_date_sp2': datetime.today()})

        # _logger.info('KEREN--->' + str(my_sp2.party))



