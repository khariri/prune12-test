from odoo import models
# from odoo.exceptions import UserError

class MutasiXlsx(models.AbstractModel):
    _name = 'report.djbc.mutasi_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        # raise UserError("yes working...")
        sheet = workbook.add_worksheet('Mutasi')
        format1 = workbook.add_format({'font_size':12, 'align':'vcenter', 'bold':True})
        format2 = workbook.add_format({'font_size':12, 'align':'vcenter'})
        sheet.write(0,0,'Laporan Mutasi',format1)
        sheet.write(1,0, 'Periode: ' + str(data['form']['date_start']) + ' s.d. ' + str(data['form']['date_start']), format1)
        sheet.write(2,0,'Kode Barang',format1)
        sheet.write(2,1,'Nama Barang',format1)
        sheet.write(2,2,'Saldo Awal',format1)
        sheet.write(2,3,'Pemasukan',format1)
        sheet.write(2,4,'Pengeluaran',format1)
        sheet.write(2,5,'Penyesuaian',format1)
        sheet.write(2,6,'Stock Opname',format1)
        sheet.write(2,7,'Saldo Akhir',format1)
        sheet.write(2,8,'Selisih',format1)
        sheet.write(2,9,'Keterangan',format1)
        sheet.write(2,10,'Warehouse',format1)
        i=2
        lines = self.env['djbc.mutasi'].search([])
        for obj in lines:
            i=i+1
            sheet.write(i,0,obj.kode_barang,format2)
            sheet.write(i,1,obj.nama_barang,format2)
            sheet.write(i,2,obj.saldo_awal,format2)
            sheet.write(i,3,obj.pemasukan,format2)
            sheet.write(i,4,obj.pengeluaran,format2)
            sheet.write(i,5,obj.penyesuaian,format2)
            sheet.write(i,6,obj.stock_opname,format2)
            sheet.write(i,7,obj.saldo_akhir,format2)
            sheet.write(i,8,obj.selisih,format2)
            sheet.write(i,9,obj.keterangan,format2)
            sheet.write(i,10,obj.warehouse,format2)
            
