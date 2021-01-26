import logging
import requests
from datetime import datetime

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class PRSendSP2Wizard(models.TransientModel):
    _name='pr.send.sp2.wizard'

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
    def send_sp2(self):

        # data = {
        #    'model': 'pr.send.sp2.wizard',
        #    'form': self.read()[0]
        # }

        # my_sp2 = self.browse(self.env.context.get('active_id'))

        my_sp2 = self.env['djbc.docs'].browse(self.env.context.get('active_id'))
        # _logger.info('KEREN--->' + str(my_sp2.party))

        if (my_sp2.is_finished):
            _is_finished = 1
        else:
            _is_finished = 0


        payload = '{ '

        if my_sp2.kd_document_type :
            payload = payload + '"kd_document_type":"' + str(my_sp2.kd_document_type) + '",'

        payload = payload + '"npwpCargoOwner":"' + str(my_sp2.npwpCargoOwner) + '",'

        if my_sp2.nm_cargoowner:
            payload = payload +'"nm_cargoowner":"' + str(my_sp2.nm_cargoowner.name) + '",'

        if my_sp2.no_dok:
            payload = payload + '"document_no":"' + str(my_sp2.no_dok) + '",'

        if my_sp2.tgl_dok:
            payload = payload + '"document_date":"' + \
                      my_sp2.tgl_dok.strftime("%Y-%m-%d") + '", '

        if my_sp2.no_doc_release:
            payload = payload + '"no_doc_release":"' + str(my_sp2.no_doc_release) + '", '

        if my_sp2.date_doc_release:
            payload = payload + '"date_doc_release":"' + \
                      my_sp2.date_doc_release.strftime("%Y-%m-%d") + '", '

        if my_sp2.document_state:
            payload = payload + '"document_status":"' + str(my_sp2.document_state) + '", '

        if my_sp2.no_bl:
            payload = payload + '"bl_no":"' + str(my_sp2.no_bl) + '", '

        if my_sp2.tgl_bl:
            payload = payload + '"bl_date":"' + my_sp2.tgl_bl.strftime("%Y-%m-%d") + '", '


        payload = payload + '"id_platform":"' + str(my_sp2.id_platform) + '",'

        if my_sp2.terminal:
            payload = payload + '"terminal":"' + str(my_sp2.terminal) + '",'

        if my_sp2.paid_thrud_date:
            payload = payload + '"paid_thrud_date": "' + \
                      my_sp2.paid_thrud_date.strftime("%Y-%m-%d") + '",'

        if my_sp2.proforma:
            payload = payload + '"proforma":"' + str(my_sp2.proforma) + '",'

        if my_sp2.proforma_date:
            payload = payload + '"proforma_date": "' + \
                      my_sp2.proforma_date.strftime("%Y-%m-%d") + '",'

        if my_sp2.price:
            payload = payload + '"price": "' + str(my_sp2.price) + '",'

        if my_sp2.status:
            payload = payload + '"status": "' + str(my_sp2.status) + '",'

        payload = payload + '"is_finished": "' + str(_is_finished) + '",'

        if my_sp2.party:
            payload = payload + '"party": "' + str(my_sp2.party) + '",'

        payload = payload + '"container": ['

        for cont_id in my_sp2.container_ids:

            payload = payload + '{"container_no": "' + str(cont_id.name) + '",'

            if cont_id.container_size:
                payload = payload + '"container_size": "' + str(cont_id.container_size) + '",'

            if cont_id.container_type:
                payload = payload + '"container_type": "' + str(cont_id.container_type) + '",' \

            payload = payload + '"gate_pass": "' + str(cont_id.gate_pass) + '"},'



        payload = payload[:-1]
        payload = payload + ']}'



        if self.server_tujuan=='dev':
            # headers = {'key': "tes", 'content-type': "application/json"}
            # r = requests.post("https://esbbcext01.beacukai.go.id:8090/document_sp2/final/",
            #                  payload, headers=headers)
            r = "Success."
        else:
            headers = {'key': self.api_key, 'content-type': "application/json"}
            r = requests.post("https://nlehub.kemenkeu.go.id/V1/NLE/document_sp2",
                              payload, headers=headers)

        # pp = pprint.PrettyPrinter(indent=4)
        my_sp2.write({"keterangan": r + '\n' + payload})
        if r=='Success.':
            my_sp2.write({"state": 'sent_sp2'})
            my_sp2.write({"sent_sp2_date": datetime.today()})

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
