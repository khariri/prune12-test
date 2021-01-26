import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)


class DJBCKiteMasukBb(models.Model):
    _name = 'djbc.kite.masuk.bb'
    _description = 'Laporan Pemasukan Bahan Baku'
    _rec_name = 'no_dok'

    jenis_dok = fields.Char(string='Jenis Dokumen')
    no_dok = fields.Char(string='Nomor Dokumen')
    tgl_dok = fields.Date(string='Tgl Dokumen')
    no_seri = fields.Char(string="No Seri", required=False, )
    no_penerimaan = fields.Char(string='Nomor Penerimaan')
    tgl_penerimaan = fields.Date(string='Tgl Penerimaan')
    kode_barang = fields.Char(string='Kode Barang')
    nama_barang = fields.Char(string='Nama Barang')
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    nilai = fields.Float(string='Nilai')
    currency = fields.Char(string='Mata Uang')
    warehouse = fields.Char(string='Gudang')
    penerima_subkon = fields.Char(string="Penerima Subkontrak", required=False, )
    negara_asal = fields.Char(string="Negara Asal Barang", required=False, )
