import logging
from datetime import datetime
import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class CreateInvDOWizard(models.TransientModel):
    _name='create.inv.do.wizard'

    price_do = fields.Float(string="Price",  required=False, )

    @api.multi
    def create_inv_do(self):

        my_do = self.env['djbc.docs'].browse(self.env.context.get('active_id'))
        my_inv = self.env['account.invoice'].create({'partner_id': my_do.nm_cargoowner.id,
                                                     'currency_id': 12})
        # _logger.info(str(my_inv.id))
        self.env['account.invoice.line'].create({'invoice_id': my_inv.id,
                                                 'name': "pengurusan DO",
                                                 'account_id': 19,
                                                 'quantity': 1,
                                                 'price_unit': self.price_do, })
        # self.write({'state':"wait_sp2"})
        my_do.write({'invoice_do_id': my_inv.id})
        my_do.write({'state': "wait_do"})
        my_do.write({'price_do':self.price_do})
        my_do.write({'status_do': 'Invoiced'})

        # _logger.info('KEREN--->' + str(my_sp2.party))



