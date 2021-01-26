CREATE OR REPLACE FUNCTION djbc_posisi_wip()
RETURNS VOID AS $BODY$

DECLARE
	--csr cursor for
		   
BEGIN
	delete from djbc_posisi_wip;
	--select * from djbc_posisi_wip;
	insert into djbc_posisi_wip (tgl_penerimaan, kode_barang, nama_barang, jumlah,
		satuan, warehouse) 
		select x.date, z.default_code, z.name, x.product_uom_qty, xa.name as satuan,  
		xb.name as warehouse from stock_move x 
		join product_product y on y.id=x.product_id
		join product_template z on z.id=y.product_tmpl_id
		join uom_uom xa on xa.id=x.product_uom
		join stock_warehouse xb on xb.id=x.warehouse_id
		where x.state='assigned' and x.reference like '%MO%';
		
		
		
		
END;


$BODY$
LANGUAGE plpgsql;

select * from djbc_posisi_wip();