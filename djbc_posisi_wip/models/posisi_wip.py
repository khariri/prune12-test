import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class DJBCPosisiWIP(models.Model):
    _name = 'djbc.posisi.wip'
    _description = 'DJBC Laporan Posisi WIP'

    tgl_penerimaan = fields.Date(string='Tgl Penerimaan')
    kode_barang = fields.Char(string='Kode Barang')
    nama_barang = fields.Char(string='Nama Barang')
    jumlah = fields.Float(string='Jumlah')
    satuan = fields.Char(string='Satuan')
    warehouse = fields.Char(string='Warehouse')

    @api.model_cr
    def init(self):
        self.env.cr.execute("""
        DROP FUNCTION IF EXISTS djbc_posisi_wip(DATE, DATE);
       CREATE OR REPLACE FUNCTION djbc_posisi_wip(date_start DATE, date_end DATE)
RETURNS VOID AS $BODY$

DECLARE
	
	csr cursor for
		select xx.id, y.date_done as tgl_penerimaan, 
		xz.default_code as kode_barang, xz.name as nama_barang,
		xx.product_uom_qty as jumlah, yx.name as satuan, t8.name as warehouse
		from stock_picking y
		join stock_move xx on xx.picking_id=y.id
		join stock_location t5 on t5.id = xx.location_id
                	join stock_location t8 on t8.id = t5.location_id	
		join product_product xy on xy.id=xx.product_id
		join product_template xz on xz.id=xy.product_tmpl_id
		join uom_uom yx on yx.id=xx.product_uom
		join stock_picking_type t1 on t1.id=y.picking_type_id
		where xx.state='done' and t1.name like '%Pick Components'
		and date(y.date_done) >= date_start and date(y.date_done)<=date_end;
	
	
			
begin

	delete from djbc_posisi_wip;
	
	
	  for rec in csr loop
		insert into djbc_posisi_wip (tgl_penerimaan, kode_barang,
			nama_barang, jumlah, satuan, warehouse) 
			values (rec.tgl_penerimaan, rec.kode_barang, rec.nama_barang, rec.jumlah, rec.satuan, rec.warehouse) ;
	  end loop;


end;

$BODY$
LANGUAGE plpgsql;
        """)

    #def call_djbc_posisi_wip(self):
    #    cr = self.env.cr
    #    cr.execute("select djbc_posisi_wip()")
    #    return {
    #        'name': 'Laporan Posisi WIP',
    #        'domain': [],
    #        'view_type': 'form',
    #        'res_model': 'djbc.posisi.wip',
    #        'view_id': False,
    #        'view_mode': 'tree,form',
    #        'type': 'ir.actions.act_window',
    #    }
