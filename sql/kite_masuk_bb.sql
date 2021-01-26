CREATE OR REPLACE FUNCTION djbc_kite_masuk_bb(date_start DATE, date_end DATE, v_wh TEXT)
RETURNS VOID AS $BODY$
DECLARE
	
		   
BEGIN
	delete from djbc_kite_masuk_bb; 
	insert into djbc_kite_masuk_bb (no_dok, tgl_dok, jenis_dok, no_seri, no_penerimaan, 
		tgl_penerimaan, kode_barang,
		nama_barang, jumlah, satuan, nilai, currency, warehouse, penerima_subkon, negara_asal)
		select no_dok, tgl_dok, jenis_dok,'no seri', y.name as no_penerimaan, y.date_done as tgl_penerimaan, 
		xz.default_code as kode_barang, xz.name as nama_barang,
		xx.product_uom_qty as jumlah, yx.name as satuan, yz.price_subtotal as nilai, 
		zx.name as currency, 'wh1', 'penerima subkon', 'negara asal'
		from djbc_docs x
		join stock_picking y on x.id=y.docs_id
		join res_partner z on z.id=y.partner_id
		join stock_move xx on xx.picking_id=y.id
		join product_product xy on xy.id=xx.product_id
		join product_template xz on xz.id=xy.product_tmpl_id
		join uom_uom yx on yx.id=xx.product_uom
		join purchase_order_line yz on yz.id=xx.purchase_line_id
		join res_currency zx on zx.id=yz.currency_id
		--where (jenis_dok='bc20' or jenis_dok='bc23') 
		--and tgl_dok>=date_start and tgl_dok<=date_end
		order by x.tgl_dok;
END;

$BODY$
LANGUAGE plpgsql;

