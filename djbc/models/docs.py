from odoo import models, fields, api
# from datetime import datetime
import requests
# import pprint
import logging
_logger = logging.getLogger(__name__)

class DJBCDocs(models.Model):
    _name='djbc.docs'
    _description='DJBC Documents'
    _rec_name='no_dok'

    no_dok = fields.Char(string='Nomor Dokumen BC', required=True,)
    tgl_dok = fields.Date(string='Tanggal Dokumen BC', required=True,)
    jenis_dok = fields.Many2one(comodel_name="djbc.doctype", string="Doc Type", required=True, )
    no_aju = fields.Char(string="Nomor Pengajuan", required=False, )
    tgl_aju = fields.Date(string="Tanggal Pengajuan", required=False, )
    no_bl = fields.Char(string="Nomor B/L", required=False, )
    tgl_bl = fields.Date(string="Tanggal B/L", required=False, )
    jenis_bl = fields.Selection(
        string="Jenis B/L",
        selection=[
            ("master", "Master"),
            ("house", "House"),
        ],
        required=False,
        default="house",
    )
    no_cont = fields.Char(string="Nomor Container", required=False, )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("req_do", "DO Request"),
            ("wait_do", "DO Invoiced"),
            ("paid_do", "DO Paid"),
            ("sent_do", "DO Sent"),
            ("req_sp2", "SP2 Request"),
            ("wait_sp2", "SP2 Invoiced"),
            ("paid_sp2", "SP2 Paid"),
            ("sent_sp2", "SP2 Sent"),
        ],
        required=True,
        default="draft",
    )

    kd_document_type = fields.Integer(string="Kode Document Type", required=False, )
    npwpCargoOwner = fields.Char(string='NPWP Cargo Owner', required=False, )
    # npwpCargoOwner = fields.Many2one(comodel_name="res.partner", string="NPWP Cargo Owner", required=True, )
    nm_cargoowner = fields.Many2one(comodel_name="res.partner", string="Nama Cargo Owner", required=False,
                                    domain=[('nle_category', '=', 'consignee'),])
    no_doc_release = fields.Char(string='Doc Release No', required=False,)
    date_doc_release = fields.Date(string='Doc Release Date', required=False,)
    document_state = fields.Char(string='Document Status', required=False,)
    id_platform = fields.Char(string='Id Platform', required=False, default='XXXXX')
    # terminal = fields.Char(string='Terminal', required=False,)
    terminal = fields.Many2one(comodel_name="res.partner", string="Terminal", required=False,
                               domain=[('nle_category', '=', 'terminal'), ])
    paid_thrud_date = fields.Date(string='Paid Date', required=False,)
    proforma = fields.Char(string='Proforma', required=False,)
    price = fields.Float(string="Price",  required=False, )
    proforma_date = fields.Date(string='Proforma Date', required=False,)
    sent_sp2_date = fields.Date(string='Tgl Kirim SP2', required=False, )
    status = fields.Char(string='Status', required=False,)
    is_finished = fields.Boolean(string='Is Finished?', required=False, default=False)
    party = fields.Integer(string='Jumlah Container', required=False, )
    keterangan = fields.Text(string="Keterangan", required=False, )
    container_ids = fields.One2many(comodel_name="djbc.containers", inverse_name="doc_id",string="Container List", required=False, )

    # tambahan dari DO
    request_date = fields.Date(string='Request DO Date', required=False, )
    request_date_sp2 = fields.Date(string='Request SP2 Date', required=False, )
    id_ff_ppjk = fields.Char (string='NPWP FF/PPJK', required=False, )
    # shipping_name = fields.Char (string='Shipping Line', required=False, )
    shipping_name = fields.Many2one(comodel_name="res.partner", string="Shipping Name", required=False,
                    domain=[('nle_category', '=', 'shipping'), ])
    forwarder_name = fields.Many2one(comodel_name="res.partner", string="Nama FF/PPJK", required=False,
                                    domain=[('nle_category', '=', 'ppjk'),])
    price_do = fields.Float(string='Price DO', required=False, )
    paid_date_do = fields.Date(string='Paid Date DO', required=False, )
    status_do = fields.Char(string='Status DO', required=False, )
    # status_do = fields.Selection(
    #    string="Status DO",
    #    selection=[
    #        ("Request", "Request"),
    #        ("Invoiced", "Invoiced"),
    #        ("Finish", "Finish"),
    #    ],
    #    required=False,
    #    default="Request",
    # )
    do_number = fields.Char(string='Nomor DO', required=False, )
    do_date_number = fields.Date(string='Tgl DO', required=False, )
    sent_do_date = fields.Date(string='Tgl Kirim DO', required=False, )



    @api.onchange('nm_cargoowner')
    @api.multi
    def onchange_nm_cargoowner(self):
        self.npwpCargoOwner = self.nm_cargoowner.vat

    @api.onchange('forwarder_name')
    @api.multi
    def onchange_forwarder_name(self):
        self.id_ff_ppjk = self.forwarder_name.vat





        


