import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCNofasMasuk(models.Model):
    _name = 'djbc.nofas_masuk'
    _description = 'DJBC Laporan Pemasukan'
    _rec_name = 'no_dok'

    jenis_dok = fields.Char(string='Jenis Dokumen')
    no_aju = fields.Char(string='Nomor Aju')
    tgl_aju=fields.Date(string='Tgl Aju')
    no_dok=fields.Char (string='Nomor Pendaftaran')
    # no_dok  = fields.Many2one(comodel_name="djbc.docs", string="Nomor Pendaftaran", required=False, )
    tgl_dok=fields.Date(string='Tgl Pendaftaran')
    no_penerimaan = fields.Many2one(comodel_name="stock.picking", string="Nomor Penerimaan", required=False, )
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
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    jumlah_kemasan = fields.Float(string='Jumlah Kemasan')
    satuan_kemasan = fields.Char(string='Satuan Kemasan') 
    nilai = fields.Float(string='Nilai')
    currency = fields.Char(string='Currency')
    location = 	fields.Char(string='Location')
    warehouse = fields.Char(string='Warehouse')
    alm_wh = fields.Char(string='Alamat Warehouse')
    kota_wh = fields.Char(string='Kota')
    # qty_sisa=fields.Float(string='Sisa')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_nofas_masuk(DATE, DATE);
        CREATE OR REPLACE FUNCTION djbc_nofas_masuk(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$
DECLARE
	
	csr cursor for
		select t3.code as jenis_dok, t2.id as lot_id, xx.id, x.no_dok as no_dok, 
			tgl_dok, y.id as no_penerimaan, 
			y.date_done as tgl_penerimaan, 
			z.name as pengirim, xz.default_code as kode_barang, xz.name as nama_barang,
			xx.product_uom_qty as jumlah, yx.name as satuan, 
			yz.price_subtotal as nilai, zx.name as currency,
			no_bl, tgl_bl, no_aju, tgl_aju, no_cont,
			xx.jumlah_kemasan as jumlah_kemasan, xx.satuan_kemasan as satuan_kemasan,
			t4.code as hs_code, t5.name as location, t7.name as pemilik, t8.name as warehouse,
			t9.street as alm_wh, t9.city as kota_wh 
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
		join purchase_order_line yz on yz.id=xx.purchase_line_id
		join res_currency zx on zx.id=yz.currency_id
		where xx.state='done' 
		-- and t6.move_type like 'in'
		and x.tgl_dok >= date_start and x.tgl_dok<=date_end
		order by x.tgl_dok;
	
	v_wh text;
		   
BEGIN
	delete from djbc_nofas_masuk;
	-- v_wh='WH/Stock';
	
	for rec in csr loop
		insert into djbc_nofas_masuk (no_dok, tgl_dok,jenis_dok,no_penerimaan, tgl_penerimaan, pengirim, kode_barang,
			nama_barang, jumlah, satuan, nilai, currency, warehouse, lot_id, no_bl, tgl_bl, no_aju, tgl_aju, no_cont,
			jumlah_kemasan, satuan_kemasan, hs_code, pemilik, location, alm_wh, kota_wh) 
			values (rec.no_dok, rec.tgl_dok, rec.jenis_dok, rec.no_penerimaan, rec.tgl_penerimaan,
				rec.pengirim, rec.kode_barang, rec.nama_barang, rec.jumlah, rec.satuan, 
				rec.nilai, rec.currency, rec.warehouse, rec.lot_id, rec.no_bl, rec.tgl_bl, 
				rec.no_aju, rec.tgl_aju, rec.no_cont, rec.jumlah_kemasan, rec.satuan_kemasan, rec.hs_code,
				rec.pemilik, rec.location, rec.alm_wh, rec.kota_wh) ;
		-- update stock_move set djbc_masuk_flag=TRUE where id=rec.id;
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
