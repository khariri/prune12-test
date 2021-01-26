import logging
from datetime import datetime
import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class NLESendDOWizard(models.TransientModel):
    _name='nle.send.do.wizard'

    server_tujuan = fields.Selection(
        string="Server Tujuan",
        selection=[
            ("dev", "Development"),
            ("prod", "Production"),
        ],
        required=True,
        default="dev",
    )
    api_key = fields.Char(string="API Key", required=False, )

    @api.multi
    def send_do(self):

        # data = {
        #    'model': 'pr.send.sp2.wizard',
        #    'form': self.read()[0]
        # }

        # my_sp2 = self.browse(self.env.context.get('active_id'))

        my_do = self.env['djbc.docs'].browse(self.env.context.get('active_id'))
        # _logger.info('KEREN--->' + str(my_do.party))


        payload = '{ '

        
        payload = payload + '"id_platform":"' + str(my_do.id_platform) + '",'

        payload = payload + '"npwpCargoOwner":"' + str(my_do.npwpCargoOwner) + '",'

        payload = payload + '"id_ff_ppjk":"' + str(my_do.id_ff_ppjk) + '",'

        payload = payload + '"shipping_name":"' + str(my_do.shipping_name.name) + '",'

        payload = payload + '"forwarder_name":"' + str(my_do.forwarder_name.name) + '",'

        payload = payload + '"party":"' + str(my_do.party) + '",'

        payload = payload + '"bl_no":"' + str(my_do.no_bl) + '",'

        payload = payload + '"bl_type":"' + str(my_do.jenis_bl) + '",'

        payload = payload + '"container": ['

        for cont_id in my_do.container_ids:

            payload = payload + '{"container_no": "' + str(cont_id.name) + '",'

            payload = payload + '"container_size": "' + str(cont_id.container_size) + '",'

            payload = payload + '"container_type": "' + str(cont_id.container_type) + '"},' 

        payload = payload[:-1]
        payload = payload + ']}'

        # if self.server_tujuan=='dev':
        #    headers = {'key': "tes", 'content-type': "application/json"}
        #    r = requests.post("https://esbbcext01.beacukai.go.id:8090/document_sp2/final/",
        #                      payload, headers=headers)
        #else:
        #    headers = {'key': self.api_key, 'content-type': "application/json"}
        #    r = requests.post("https://nlehub.kemenkeu.go.id/V1/NLE/document_sp2",
        #                      payload, headers=headers)

        # pp = pprint.PrettyPrinter(indent=4)

        my_do.write({"keterangan": 'Success.' + '\n' + payload})
        my_do.write({"state":'sent_do'})
        my_do.write({"sent_do_date":datetime.today()})


        # return self.env['djbc.docs'].send_sp2(data=data)

    @api.onchange('api_key')
    @api.multi
    def onchange_api_key(self):
        res = {}
        if (not self.api_key) and (self.server_tujuan=='prod'):
            res = {'warning': {
                'title': ('Warning'),
                'message': ('Api Key wajib diisi jika server tujuan Production')}}
        if res:
            return res
