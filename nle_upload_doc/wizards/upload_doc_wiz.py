import logging
import xlrd
import tempfile
import binascii
from odoo import exceptions
import base64
from datetime import datetime
import requests

from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class UploadDocWizard(models.TransientModel):
    _name='upload.doc.wizard'

    file_data = fields.Binary(string="Pilih File",  )
    kd_document_type = fields.Selection(
        string="Jenis Dokumen",
        selection=[
            ("3", "BC 1.6"),
            ("2", "BC 2.3"),
        ],
        required=True,
        default="2",
    )

    @api.multi
    def upload_doc(self):

        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(self.file_data))
        fp.seek(0)
        # fp = tempfile.TemporaryFile('w+')
        # fp.write(base64.decodebytes(self.file_data))
        # vals = {}

        # To open Workbook

        wb = xlrd.open_workbook(fp.name)

        header = wb.sheet_by_index(0)
        dokumen = wb.sheet_by_index(4)
        respon = wb.sheet_by_index(7)
        # barang = wb.sheet_by_index(1)
        kontainer = wb.sheet_by_index(6)


        jml_row_header = header.nrows
        jml_row_respon = respon.nrows
        # jml_row_barang = barang.nrows
        jml_row_dokumen = dokumen.nrows
        jml_row_kontainer = kontainer.nrows

        
        # raise exceptions.UserError("Jumlah Row Header: " + str(jml_row_header-1))
        # id_ff_ppjk = '123456789033000'
        jenis_dok_ids = self.env['djbc.doctype'].search(
            [('kd_document_type', '=', self.kd_document_type)],limit=1)
        jenis_dok = jenis_dok_ids[0]
        # raise exceptions.UserError(str(jenis_dok) + ' dan ' + str(jenis_dok.id))


        for row_header in range(1, jml_row_header):

            nomor_aju = header.cell_value(row_header, 0)
            # raise exceptions.UserError("Nomor Aju: ", nomor_aju)
            perusahaan = header.cell_value(row_header, 2)
            no_dok = header.cell_value(row_header, 103)
            tgl_dok = header.cell_value(row_header, 117)
            # npwp pemilik header kolom AH
            npwp_cargo_owner = header.cell_value(row_header, 33)
            # nama pemilik kolom CM
            # nama_cargo_owner = header.cell_value(row_header, 90)

            _logger.info('search id Cargo Owner')
            partner_ids = self.env['res.partner'].search(
                [('vat', '=', npwp_cargo_owner)], limit=1)

            if not partner_ids:
                raise exceptions.UserError("NPWP Cargo Owner tidak ditemukan" + str(npwp_cargo_owner))

            else:
                _logger.info("npwp Cargo Owner ditemukan")
                id_cargo_owner = partner_ids[0]
                _logger.info("ID Cargo Owner: " + str(id_cargo_owner))

            

            # search dokumen bl(705)
            for row_dokumen in range(1, jml_row_dokumen):
                no_aju_dokumen = dokumen.cell_value(row_dokumen, 0)
                kode_jenis_dokumen = dokumen.cell_value(row_dokumen, 3)

                if no_aju_dokumen == nomor_aju and kode_jenis_dokumen == '705':
                    no_bl = dokumen.cell_value(row_dokumen, 4)
                    _logger.info("Nomor BL: " + str(no_bl))
                    tgl_bl = dokumen.cell_value(row_dokumen, 5)
                    break

            # search dokumen invoice(380)
            for row_dokumen in range(1, jml_row_dokumen):
                no_aju_dokumen = dokumen.cell_value(row_dokumen, 0)
                kode_jenis_dokumen = dokumen.cell_value(row_dokumen, 3)

                if no_aju_dokumen == nomor_aju and kode_jenis_dokumen == '380':
                    proforma = dokumen.cell_value(row_dokumen, 4)
                    _logger.info("Proforma: " + str(proforma))
                    proforma_date = dokumen.cell_value(row_dokumen, 5)

                    break

            # search Document Release No
            for row_res in range(1, jml_row_respon):
                no_aju_res = respon.cell_value(row_res, 0)
                if no_aju_res == nomor_aju:
                    no_doc_release = respon.cell_value(row_res, 2)
                    _logger.info("Document Release No: " + str(no_doc_release))
                    date_doc_release = respon.cell_value(row_res, 3)

                    break

            doc_ids = self.env['djbc.docs'].search(
                [('no_dok', '=', no_dok),('tgl_dok', '=', tgl_dok),
                 ('jenis_dok', '=', jenis_dok.id)], limit=1)

            if not doc_ids:
                # _logger.info(str(no_dok) + "tidak ditemukan")
                # raise exceptions.UserError(str(jenis_dok) + ' dan ' + str(jenis_dok.id))

                doc_id = self.env['djbc.docs'].create({'no_dok': no_dok,
                                                       'jenis_dok': jenis_dok.id,
                      'tgl_dok': tgl_dok, 'no_bl': no_bl, 'tgl_bl': tgl_bl,
                      'npwpCargoOwner': npwp_cargo_owner, 'document_state': 'SPPB',
                      'nm_cargoowner': id_cargo_owner.id, 
                      'kd_document_type': self.kd_document_type, 'no_doc_release': no_doc_release,
                      'date_doc_release': date_doc_release,
                      'proforma': proforma, 'proforma_date': proforma_date,
                      'no_aju': nomor_aju})

                _logger.info("Doc Id created is: " + str(doc_id))

            else:
                _logger.info(str(no_dok)+ "ditemukan")
                doc_id = doc_ids[0]
                _logger.info("Doc Id: " + str(doc_id))

            _logger.info('search id PPJK')
            
            id_ff_ppjk = header.cell_value(row_header, 37)
            forwarder_name_ids = self.env['res.partner'].search(
                [('vat', '=', id_ff_ppjk)], limit=1)

            if not forwarder_name_ids:
                # raise exceptions.UserError('NPWP PPJK tidak ditemukan')
                _logger.info("NPWP PPJK tidak ditemukan")
            
            else:
                # _logger.info("NPWP PPJK ditemukan")
                forwarder_name = forwarder_name_ids[0]
                # _logger.info("ID PPJK: " + str(forwarder_name[0]))
                # update djbc.docs set forwarder_name.id dan id_ff_ppjk
                my_doc = self.env['djbc.docs'].browse(doc_id.id)
                my_doc.write({'forwarder_name':forwarder_name.id})
                my_doc.write({'id_ff_ppjk':id_ff_ppjk})

            # add kontainer
            for row_kontainer in range(1, jml_row_kontainer):
                no_aju_kontainer = kontainer.cell_value(row_kontainer, 0)
                if no_aju_kontainer == nomor_aju:
                    container_no = kontainer.cell_value(row_kontainer, 10)
                    _logger.info("Container No: ", container_no)
                    container_size = kontainer.cell_value(row_kontainer, 6)
                    _logger.info("Container Size: ", container_size)
                    container_type = kontainer.cell_value(row_kontainer, 5)
                    _logger.info("Container Size: ", container_type)
                    cont_id = self.env['djbc.containers'].create({'name': container_no, 'container_size': container_size,
                          'container_type': container_type, 'doc_id': doc_id.id})

        # waction = self.env.ref("djbc_mutasi.""mutasi_action")
        # result = waction.read()[0]
        return self.env.ref("djbc.djbc_docs_action").read()[0]