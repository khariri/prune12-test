import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCNofasPosisi(models.Model):
    _name = 'djbc.nofas_posisi'
    _description = 'DJBC Laporan Posisi Barang'
    _rec_name = 'no_dok_masuk'

    no_urut = fields.Integer(String='No Urut')
    jenis_dok_masuk = fields.Char(string='Jenis Dokumen Masuk')
    no_aju_masuk = fields.Char(string='Nomor Aju Masuk')
    tgl_aju_masuk = fields.Date(string='Tgl Aju Masuk')
    no_dok_masuk=fields.Char (string='Nomor Dokumen Masuk')
    # no_dok  = fields.Many2one(comodel_name="djbc.docs", string="Nomor Pendaftaran", required=False, )
    tgl_dok_masuk=fields.Date(string='Tgl Dokumen Masuk')
    # no_penerimaan = fields.Many2one(comodel_name="stock.picking", string="Nomor Penerimaan", required=False, )
    no_penerimaan = fields.Char (string='Nomor Penerimaan')
    tgl_penerimaan=fields.Date(string='Tgl Penerimaan')
    no_bl = fields.Char(string='Nomor B/L')
    tgl_bl = fields.Date(string='Tgl B/L')
    no_cont = fields.Char(string='Nomor Container')
    # no_penerimaan=fields.Char(string='Nomor Penerimaan')
    pengirim = fields.Char(string='Pengirim Barang')
    pemilik = fields.Char(string='Pemilik Barang')
    hs_code = fields.Char(string='HS Code')
    kode_barang=fields.Char(string='Kode Barang')
    nama_barang=fields.Char(string='Nama Barang')
    lot_id = fields.Many2one(comodel_name="stock.production.lot", string="Lot No", required=False, )
    jumlah_pemasukan = fields.Float(string='Jumlah Pemasukan')
    satuan_pemasukan = fields.Char(string='Satuan Pemasukan')
  
    nilai_masuk = fields.Float(string='Nilai Masuk')
    currency_masuk = fields.Char(string='Currency Masuk')

    jumlah_kemasan_masuk = fields.Float(string='Jumlah Kemasan Masuk')
    satuan_kemasan_masuk = fields.Char(string='Satuan Kemasan Masuk')
    jenis_dok_keluar = fields.Char(string='Jenis Dokumen Keluar')
    no_aju_keluar = fields.Char(string='Nomor Aju Keluar')
    tgl_aju_keluar = fields.Date(string='Tgl Aju Keluar')	
    no_dok_keluar = fields.Char (string='Nomor Dokumen Keluar')
    tgl_dok_keluar = fields.Date(string='Tgl Dokumen Keluar')
    no_pengeluaran = fields.Char (string='Nomor Pengeluaran')
    tgl_pengeluaran = fields.Date(string='Tgl Pengeluaran')
    penerima = fields.Char(string='Penerima Barang')
    jumlah_pengeluaran = fields.Float(string='Jumlah Pengeluaran')
    satuan_pengeluaran = fields.Char(string='Satuan Pengeluaran')

    nilai_keluar = fields.Float(string='Nilai Keluar')
    currency_keluar = fields.Char(string='Currency Keluar')

    jumlah_kemasan_keluar = fields.Float(string='Jumlah Kemasan Keluar')
    satuan_kemasan_keluar = fields.Char(string='Satuan Kemasan Keluar')   
    tgl_so = fields.Date(string='Tgl Stock Opname')
    jumlah_satuan = fields.Float(string='Jumlah Stock Opname')
    jumlah_kemasan = fields.Float(string='Jumlah Kemasan')
    selisih_satuan = fields.Float(string='Selisih Satuan')
    selisih_kemasan = fields.Float(string='Selisih Kemasan')
    sisa_satuan = fields.Float(string='Sisa Satuan')
    sisa_kemasan = fields.Float(string='Sisa Kemasan')      	
    location = 	fields.Char(string='Location')
    warehouse = fields.Char(string='Warehouse')
    alm_wh = fields.Char(string='Alamat Warehouse')
    kota_wh = fields.Char(string='Kota')
    # qty_sisa=fields.Float(string='Sisa')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_nofas_posisi(DATE, DATE);
        DROP FUNCTION IF EXISTS get_csr_keluar(varchar, date, varchar, varchar, timestamp, varchar, 
	varchar, varchar, numeric, varchar, varchar, integer, varchar, date, varchar,	
	date, varchar, float, varchar, varchar, varchar, varchar, varchar, varchar, float, varchar);

CREATE OR REPLACE FUNCTION get_csr_keluar(
	no_dok_masuk varchar, tgl_dok_masuk date, jenis_dok_masuk varchar,
	no_penerimaan varchar, tgl_penerimaan timestamp, pengirim varchar, 
	kode_barang varchar, nama_barang varchar, jumlah_pemasukan numeric, satuan_pemasukan varchar, 
	warehouse varchar, v_lot_id integer, no_bl varchar, tgl_bl date, no_aju_masuk varchar,	
	tgl_aju_masuk date, no_cont varchar, jumlah_kemasan_masuk float, satuan_kemasan_masuk varchar, 
	hs_code varchar, pemilik varchar, v_location varchar, alm_wh varchar, kota_wh varchar,
        nilai_masuk float, currency_masuk varchar)
RETURNS VOID AS $BODY$ 
declare
	csr_keluar cursor for 
		select   t3.code as jenis_dok_keluar, 
  			t2.id as lot_id, xx.id, x.no_dok as	no_dok_keluar, 
			x.tgl_dok as tgl_dok_keluar, x.tgl_aju as tgl_aju_keluar, x.no_aju as no_aju_keluar, 
			y.name as no_pengeluaran, 
			y.date_done as tgl_pengeluaran, 
			z.name as penerima, xz.default_code as kode_barang, xz.name as nama_barang,
			xx.product_uom_qty as jumlah_pengeluaran, yx.name as satuan_pengeluaran, 
			x.no_bl as no_bl_keluar, x.tgl_bl as tgl_bl_keluar, x.no_cont as no_cont_keluar,
			xx.jumlah_kemasan as jumlah_kemasan_keluar, xx.satuan_kemasan as satuan_kemasan_keluar,
			t4.code as hs_code, t5.name as location, t7.name as pemilik, t8.name as warehouse,
			t9.street as alm_wh, 
			t9.city as kota_wh,
                        yz.price_subtotal as nilai_keluar, zx.name as currency_keluar 
		from djbc_docs x
		join djbc_doctype t3 on t3.id = x.jenis_dok
		join stock_picking y on x.id=y.docs_id
		join stock_picking_type t6 on t6.id = y.picking_type_id
		join res_partner z on z.id=y.partner_id
		left join res_partner t7 on t7.id = y.owner_id
		join stock_move xx on xx.picking_id=y.id
		join stock_location t5 on t5.id = xx.location_dest_id
                	join stock_location t8 on t8.id = t5.location_id
		left join res_partner t9 on t9.id = t5.partner_id
		join stock_move_line t1 on t1.move_id = xx.id
		left join stock_production_lot t2 on t2.id = t1.lot_id
		join product_product xy on xy.id=xx.product_id
		join product_template xz on xz.id=xy.product_tmpl_id
		left join djbc_hscode t4 on t4.id = xz.hscode
		join uom_uom yx on yx.id=xx.product_uom
                left join sale_order_line yz on yz.id=xx.sale_line_id
		join res_currency zx on zx.id=yz.currency_id
		where xx.state='done' 
		-- and t6.move_type like 'in'
		-- and x.tgl_dok >= date_start and x.tgl_dok<=date_end
		and t3.is_import_doc=FALSE
		and t2.id = v_lot_id
		order by x.tgl_dok;

	v_sisa_satuan float;
	v_sisa_kemasan float;
        is_found_rec boolean;

begin
	v_sisa_satuan = jumlah_pemasukan;
	v_sisa_kemasan = jumlah_kemasan_masuk;
        is_found_rec := false;

	for rec2 in csr_keluar loop
		
		v_sisa_satuan = v_sisa_satuan - rec2.jumlah_pengeluaran;
   		v_sisa_kemasan = v_sisa_kemasan - rec2.jumlah_kemasan_keluar;

		insert into djbc_nofas_posisi (no_dok_masuk, tgl_dok_masuk,jenis_dok_masuk,no_penerimaan, 
			tgl_penerimaan, pengirim, kode_barang, nama_barang, jumlah_pemasukan, satuan_pemasukan, 
			warehouse, lot_id, no_bl, tgl_bl, no_aju_masuk,	tgl_aju_masuk, no_cont, 
			jumlah_kemasan_masuk, satuan_kemasan_masuk, hs_code, pemilik, 
			location, alm_wh, kota_wh,
                        nilai_masuk, currency_masuk, 
			no_dok_keluar, tgl_dok_keluar,jenis_dok_keluar,no_pengeluaran, 
			tgl_pengeluaran, penerima, jumlah_pengeluaran, satuan_pengeluaran, 
			no_aju_keluar, tgl_aju_keluar, jumlah_kemasan_keluar, 				
			satuan_kemasan_keluar, sisa_satuan, sisa_kemasan, 
			nilai_keluar, currency_keluar ) 
			values (no_dok_masuk, tgl_dok_masuk, jenis_dok_masuk, no_penerimaan, tgl_penerimaan,
				pengirim, kode_barang, nama_barang, jumlah_pemasukan, satuan_pemasukan, 
				warehouse, v_lot_id, no_bl, tgl_bl, 
				no_aju_masuk, tgl_aju_masuk, no_cont, jumlah_kemasan_masuk, satuan_kemasan_masuk, 					hs_code,
				pemilik, v_location, alm_wh, kota_wh,
				nilai_masuk, currency_masuk,	
				rec2.no_dok_keluar, rec2.tgl_dok_keluar, rec2.jenis_dok_keluar, rec2.no_pengeluaran, 					rec2.tgl_pengeluaran, rec2.penerima, rec2.jumlah_pengeluaran, rec2.satuan_pengeluaran, 
				rec2.no_aju_keluar, rec2.tgl_aju_keluar, rec2.jumlah_kemasan_keluar, rec2.satuan_kemasan_keluar,
				v_sisa_satuan, v_sisa_kemasan,
				rec2.nilai_keluar, rec2.currency_keluar) ;
    end loop;
     --- jika record ga ada do this

    if not is_found_rec then
        insert into djbc_nofas_posisi (no_dok_masuk, tgl_dok_masuk,jenis_dok_masuk,no_penerimaan, 
			tgl_penerimaan, pengirim, kode_barang, nama_barang, jumlah_pemasukan, satuan_pemasukan, 
			warehouse, lot_id, no_bl, tgl_bl, no_aju_masuk,	tgl_aju_masuk, no_cont, 
			jumlah_kemasan_masuk, satuan_kemasan_masuk, hs_code, pemilik, 
			location, alm_wh, kota_wh,
                        nilai_masuk, currency_masuk, sisa_satuan, sisa_kemasan) 
			values (no_dok_masuk, tgl_dok_masuk, jenis_dok_masuk, no_penerimaan, tgl_penerimaan,
				pengirim, kode_barang, nama_barang, jumlah_pemasukan, satuan_pemasukan, 
				warehouse, v_lot_id, no_bl, tgl_bl, 
				no_aju_masuk, tgl_aju_masuk, no_cont, jumlah_kemasan_masuk, satuan_kemasan_masuk, 					hs_code,
				pemilik, v_location, alm_wh, kota_wh,
				nilai_masuk, currency_masuk, v_sisa_satuan, v_sisa_kemasan) ;
    end if;
end;
$BODY$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION djbc_nofas_posisi(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
	
	csr cursor for
		select t3.code as jenis_dok_masuk, t2.id as lot_id, xx.id, x.no_dok as no_dok_masuk, 
			x.tgl_dok as tgl_dok_masuk, x.tgl_aju as tgl_aju_masuk, x.no_aju as no_aju_masuk, 
			y.name as no_penerimaan, 
			y.date_done as tgl_penerimaan, 
			z.name as pengirim, xz.default_code as kode_barang, xz.name as nama_barang,
			xx.product_uom_qty as jumlah_pemasukan, yx.name as satuan_pemasukan, 
			no_bl, tgl_bl, no_aju, tgl_aju, no_cont,
			xx.jumlah_kemasan as jumlah_kemasan_masuk, xx.satuan_kemasan as satuan_kemasan_masuk,
			t4.code as hs_code, t5.name as location, t7.name as pemilik, t8.name as warehouse,
			t9.street as alm_wh, t9.city as kota_wh,
                        yz.price_subtotal as nilai_masuk, zx.name as currency_masuk 
		from djbc_docs x
		join djbc_doctype t3 on t3.id = x.jenis_dok
		join stock_picking y on x.id=y.docs_id
		join stock_picking_type t6 on t6.id = y.picking_type_id
		join res_partner z on z.id=y.partner_id
		left join res_partner t7 on t7.id = y.owner_id
		join stock_move xx on xx.picking_id=y.id
		join stock_location t5 on t5.id = xx.location_dest_id
                	join stock_location t8 on t8.id = t5.location_id
		left join res_partner t9 on t9.id = t5.partner_id
		join stock_move_line t1 on t1.move_id = xx.id
		left join stock_production_lot t2 on t2.id = t1.lot_id
		join product_product xy on xy.id=xx.product_id
		join product_template xz on xz.id=xy.product_tmpl_id
		left join djbc_hscode t4 on t4.id = xz.hscode
		join uom_uom yx on yx.id=xx.product_uom
                left join purchase_order_line yz on yz.id=xx.purchase_line_id
		join res_currency zx on zx.id=yz.currency_id
		where xx.state='done' 
		-- and t6.move_type like 'in'
		and x.tgl_dok >= date_start and x.tgl_dok<=date_end
		and t3.is_import_doc=TRUE
		order by x.tgl_dok;
	
		   
BEGIN
	delete from djbc_nofas_posisi;

	
	for rec in csr loop
		
		-- untuk setiap dokumen masuk, carikan dokumen keluarnya

		perform get_csr_keluar(
			rec.no_dok_masuk, rec.tgl_dok_masuk, rec.jenis_dok_masuk,
			rec.no_penerimaan, rec.tgl_penerimaan, rec.pengirim, 
			rec.kode_barang, rec.nama_barang, rec.jumlah_pemasukan, rec.satuan_pemasukan, 
			rec.warehouse, rec.lot_id, rec.no_bl, rec.tgl_bl, rec.no_aju_masuk,	
			rec.tgl_aju_masuk, rec.no_cont, rec.jumlah_kemasan_masuk, rec.satuan_kemasan_masuk, 
			rec.hs_code, rec.pemilik,  rec.location, rec.alm_wh, rec.kota_wh, 
                        rec.nilai_masuk, rec.currency_masuk);
		
	end loop;
		
END;

$BODY$
LANGUAGE plpgsql;
        """)

    # def get_nopen(self):
    #    _logger.info("get_nopen functions...")
    #    for line_id in self.masuk_lines_ids:
    #        _logger.info(line_id.name)
    #        sp_id = self.env['stock.picking'].search([('name','=',line_id.name)])
    #        dok_bc = sp_id.docs_id.read(['no_dok','tgl_dok','jenis_dok'])
    #        if not dok_bc:
    #            _logger.info('dok_bc is empty')
    #        else:
    #            _logger.info(dok_bc[0]['no_dok'])
    #            line_id.write({'no_dok':dok_bc[0]['no_dok'],'tgl_dok':dok_bc[0]['tgl_dok'],'jenis_dok':dok_bc[0]['jenis_dok']})

    # def call_djbc_nofas_masuk(self):
    #    cr = self.env.cr
    #    cr.execute("select djbc_nofas_masuk()")
    #    return {
    #        'name': 'Laporan Pemasukan',
    #        'domain': [],
    #        'view_type': 'form',
    #        'res_model': 'djbc.nofas_masuk',
    #        'view_id': False,
    #        'view_mode': 'tree,form',
    #        'type': 'ir.actions.act_window',
    #    }
