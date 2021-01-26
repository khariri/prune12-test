import logging
from datetime import datetime
import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CreateInvSP2Wizard(models.TransientModel):
    _name='create.inv.sp2.wizard'

    price = fields.Float(string="Price",  required=False, )

    @api.multi
    def create_inv_sp2(self):

        my_sp2 = self.env['djbc.docs'].browse(self.env.context.get('active_id'))
        my_inv = self.env['account.invoice'].create({'partner_id': my_sp2.nm_cargoowner.id,
                                                     'currency_id': 12})
        # _logger.info(str(my_inv.id))
        self.env['account.invoice.line'].create({'invoice_id': my_inv.id,
                                                 'name': "pengurusan SP2",
                                                 'account_id': 19,
                                                 'quantity': 1,
                                                 'price_unit': self.price, })
        my_sp2.write({'price':self.price})
        my_sp2.write({'invoice_id': my_inv.id})
        my_sp2.write({'state':'wait_sp2'})
        my_sp2.write({'status': 'Invoiced'})

        # _logger.info('KEREN--->' + str(my_sp2.party))



