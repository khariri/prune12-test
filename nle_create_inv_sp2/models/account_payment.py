from odoo import models, fields
import logging
_logger = logging.getLogger(__name__)

class AccountPaymentInherit(models.Model):
    _inherit='account.payment'

    def action_validate_invoice_payment(self):
        # wt = self.env['model.name']
        # id_needed = wt.search([('field1', '=', 'value')]).id
        # new = wt.browse(id_needed)
        _logger.info("yes working")
        result = super(AccountPaymentInherit, self).action_validate_invoice_payment()
        my_inv = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        my_sp2_id = self.env['djbc.docs'].search([('invoice_id', '=', my_inv.id)]).id
        my_sp2 = self.env['djbc.docs'].browse(my_sp2_id)

        if my_inv.state=="paid":
            _logger.info(str(my_inv.state))
            my_sp2.write({'state': "paid_sp2"})
            my_sp2.write({'status': 'Finish'})
            my_sp2.write({'paid_thrud_date': self.payment_date})


        return result
