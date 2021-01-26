from odoo import models, fields, api


class DJBCPosisiWipWizard(models.TransientModel):
    _name = "djbc.posisi.wip.wizard"
    date_start = fields.Date(string='Date Start')
    date_end = fields.Date(string='Date End')

    @api.multi
    def call_djbc_posisi_wip(self):
        cr = self.env.cr
        cr.execute("select djbc_posisi_wip(%s,%s)",(self.date_start, self.date_end))
        waction = self.env.ref("djbc_posisi_wip.""posisi_wip_action")
        result = waction.read()[0]
        return result

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
