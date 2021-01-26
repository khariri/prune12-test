# import logging

from odoo import models, fields, api
from datetime import datetime

# _logger = logging.getLogger(__name__)

class PRBalanceSheetWizard(models.TransientModel):
    _name='pr.balance.sheet.wizard'

    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')

    date_start2 = fields.Date(string='Date Start')
    date_end2 = fields.Date(string='Date End')
    # djbc_category_id = fields.Many2one(comodel_name="djbc.categs", string="DJBC Category", required=False, )
    
    @api.multi 	
    def call_pr_balance_sheet(self):
        cr=self.env.cr
        # _logger.info(self.djbc_category_id.id)
        cr.execute("select pr_balance_sheet(%s,%s,%s,%s)",(self.date_start, self.date_end, self.date_start2, self.date_end2))
        waction = self.env.ref("pr_balance_sheet.""pr_balance_sheet_action")
        result = waction.read()[0]
        return result
    
    def generate_laporan_xls(self):
        cr=self.env.cr
        cr.execute("select pr_balance_sheet(%s,%s,%s,%s)",(self.date_start, self.date_end, self.date_start2, self.date_end2))
        data = {
            'model': 'pr.balance.sheet.wizard',
            'form': self.read()[0]
        }
        return self.env.ref('pr_balance_sheet.balance_sheet_xlsx').report_action(self, data=data)
    
    @api.onchange('date_end')
    @api.multi
    def onchange_date(self):
        res={}
        if self.date_start>self.date_end:
            res = {'warning':{
                'title':('Warning'),
                'message':('Tanggal Akhir Lebih Kecil Dari Tanggal Mulai')}}
        if res:
            return res

        


