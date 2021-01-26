from odoo import models, fields

# import logging
# _logger = logging.getLogger(__name__)

class AccountPaymentInherit(models.Model):
    _inherit='account.payment'

    # today = fields.Date(default=fields.Date.today)
    # my_date = fields.Date(string='My Date', default=lambda s: fields.Date.context_today(s))

    def action_validate_invoice_payment(self):
        # wt = self.env['model.name']
        # id_needed = wt.search([('field1', '=', 'value')]).id
        # new = wt.browse(id_needed)
        # _logger.info("yes working")
        result = super(AccountPaymentInherit, self).action_validate_invoice_payment()
        my_inv = self.env['account.invoice'].browse(self.env.context.get('active_id'))
        my_do_id = self.env['djbc.docs'].search([('invoice_do_id', '=', my_inv.id)]).id
        my_do = self.env['djbc.docs'].browse(my_do_id)

        if my_inv.state=="paid":
            # _logger.info(str(my_inv.state))
            my_do.write({'state': "paid_do"})
            my_do.write({'status_do': "Finish"})
            my_do.write({'paid_date_do': self.payment_date})


        return result
