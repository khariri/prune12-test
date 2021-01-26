from odoo import models
from odoo.exceptions import UserError


class BalanceSheetXlsx(models.AbstractModel):
    _name = 'report.balance_sheet_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        sheet2 = workbook.add_worksheet('Laba(Rugi)')
        format1 = workbook.add_format({'font_size': 12, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 12, 'align': 'vcenter'})
        sheet2.write(0, 0, 'Laba Rugi', format1)
        sheet2.write(1, 0, 'Periode', format1)
        sheet2.write(2, 0, 'Account Code', format1)
        sheet2.write(2, 1, 'Account Name', format1)
        sheet2.write(2, 2, 'Current Period', format1)
        sheet2.write(2, 3, 'Previous Period', format1)
        sheet2.write(2, 4, 'Currency', format1)
        sheet2.write(2, 5, 'Original Current Period', format1)
        sheet2.write(2, 6, 'Original Previous Period', format1)

        tot_cur_period_pendapatan = 0
        tot_prev_period_pendapatan = 0

        i = 3
        sheet2.write(i, 0, "Pendapatan", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Income')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code, format2)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, format2)
            sheet2.write(i, 3, obj.prev_period * -1, format2)
            sheet2.write(i, 4, obj.currency, format2)
            sheet2.write(i, 5, obj.ori_cur_period, format2)
            sheet2.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_pendapatan = tot_cur_period_pendapatan + obj.cur_period
            tot_prev_period_pendapatan = tot_prev_period_pendapatan + obj.prev_period
        i = i + 1
        sheet2.write(i, 0, 'Total Pendapatan', format1)
        # sheet.write(i, 1, obj.name, format2)
        tot_cur_period_pendapatan = tot_cur_period_pendapatan * -1
        tot_prev_period_pendapatan = tot_prev_period_pendapatan * -1
        sheet2.write(i, 2, tot_cur_period_pendapatan, format2)
        sheet2.write(i, 3, tot_prev_period_pendapatan, format2)

        i = i + 2
        sheet2.write(i, 0, "HPP", format1)
        tot_cur_period_hpp = 0
        tot_prev_period_hpp = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Cost of Revenue')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code, format2)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period, format2)
            sheet2.write(i, 3, obj.prev_period, format2)
            sheet2.write(i, 4, obj.currency, format2)
            sheet2.write(i, 5, obj.ori_cur_period, format2)
            sheet2.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_hpp = tot_cur_period_hpp + obj.cur_period
            tot_prev_period_hpp = tot_prev_period_hpp + obj.prev_period
        i = i + 1
        sheet2.write(i, 0, 'Total HPP', format1)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_period_hpp, format2)
        sheet2.write(i, 3, tot_prev_period_hpp, format2)

        i = i + 2
        sheet2.write(i, 0, 'Laba Kotor', format1)
        # sheet.write(i, 1, obj.name, format2)
        laba_kotor_cur_period = tot_cur_period_pendapatan-tot_cur_period_hpp
        laba_kotor_prev_period = tot_cur_period_pendapatan-tot_prev_period_hpp
        sheet2.write(i, 2, laba_kotor_cur_period , format2)
        sheet2.write(i, 3, laba_kotor_prev_period, format2)

        i = i + 2
        sheet2.write(i, 0, "Beban Adm dan Umum", format1)
        tot_cur_period_exp = 0
        tot_prev_period_exp = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Expenses')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code, format2)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period, format2)
            sheet2.write(i, 3, obj.prev_period, format2)
            sheet2.write(i, 4, obj.currency, format2)
            sheet2.write(i, 5, obj.ori_cur_period, format2)
            sheet2.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_exp = tot_cur_period_exp + obj.cur_period
            tot_prev_period_exp = tot_prev_period_exp + obj.prev_period
        i = i + 1
        sheet2.write(i, 0, 'Beban Adm dam Umum', format1)
        # sheet.write(i, 1, obj.name, format2)
        sheet2.write(i, 2, tot_cur_period_exp, format2)
        sheet2.write(i, 3, tot_prev_period_exp, format2)

        i = i + 2
        sheet2.write(i, 0, "Pendapatan Lain-lain", format1)
        tot_cur_period_oti = 0
        tot_prev_period_oti = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Other Income')])
        for obj in lines:
            i = i + 1
            sheet2.write(i, 0, obj.code, format2)
            sheet2.write(i, 1, obj.name, format2)
            sheet2.write(i, 2, obj.cur_period * -1, format2)
            sheet2.write(i, 3, obj.prev_period * -1, format2)
            sheet2.write(i, 4, obj.currency, format2)
            sheet2.write(i, 5, obj.ori_cur_period, format2)
            sheet2.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_oti = tot_cur_period_oti + obj.cur_period
            tot_prev_period_oti = tot_prev_period_oti + obj.prev_period
        i = i + 1
        sheet2.write(i, 0, 'Pendapatan Lain-lain', format1)
        # sheet.write(i, 1, obj.name, format2)
        tot_cur_period_oti = tot_cur_period_oti * -1
        tot_prev_period_oti = tot_prev_period_oti * -1
        sheet2.write(i, 2, tot_cur_period_oti, format2)
        sheet2.write(i, 3, tot_prev_period_oti, format2)

        i = i + 2
        sheet2.write(i, 0, 'Laba Bersih', format1)
        # sheet.write(i, 1, obj.name, format2)
        laba_bersih_cur_period = laba_kotor_cur_period - tot_cur_period_exp + tot_cur_period_oti
        laba_bersih_prev_period = laba_kotor_prev_period - tot_prev_period_exp + tot_prev_period_oti
        sheet2.write(i, 2, laba_bersih_cur_period, format2)
        sheet2.write(i, 3, laba_bersih_prev_period, format2)


        sheet = workbook.add_worksheet('Neraca')
        sheet.write(0,0,'Balance Sheet',format1)
        sheet.write(1,0,'Periode',format1)
        sheet.write(2,0,'Account Code',format1)
        sheet.write(2,1,'Account Name',format1)
        sheet.write(2,2,'Current Period',format1)
        sheet.write(2,3,'Previous Period',format1)
        sheet.write(2,4,'Currency',format1)
        sheet.write(2,5,'Original Current Period',format1)
        sheet.write(2,6,'Original Previous Period',format1)

        # search account type = Bank and Cash
        tot_cur_period = 0
        tot_prev_period = 0
        tot_ori_cur_period = 0
        tot_ori_prev_period = 0
        i=3
        sheet.write(i, 0, "Aktiva", format1)
        i=i+1
        sheet.write(i, 0, "Kas dan Setara Kas", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Bank and Cash')])
        for obj in lines:
            i=i+1
            sheet.write(i,0,obj.code,format2)
            sheet.write(i,1,obj.name,format2)
            sheet.write(i,2,obj.cur_period,format2)
            sheet.write(i,3,obj.prev_period,format2)
            sheet.write(i,4,obj.currency,format2)
            sheet.write(i,5,obj.ori_cur_period,format2)
            sheet.write(i,6,obj.ori_prev_period,format2)
            tot_cur_period = tot_cur_period + obj.cur_period
            tot_prev_period = tot_prev_period + obj.prev_period
            tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
            tot_ori_prev_period = tot_ori_prev_period + obj.prev_period
            # raise UserError("yes working...6")

        i = i + 1
        sheet.write(i, 0, "Aktiva Lancar", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period = tot_cur_period + obj.cur_period
            tot_prev_period = tot_prev_period + obj.prev_period
            tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
            tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        i = i + 1
        sheet.write(i, 0, "Bayar Di Muka", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Prepayments')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period = tot_cur_period + obj.cur_period
            tot_prev_period = tot_prev_period + obj.prev_period
            tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
            tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        i = i + 1
        sheet.write(i, 0, "Aktiva Tetap", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Fixed Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period = tot_cur_period + obj.cur_period
            tot_prev_period = tot_prev_period + obj.prev_period
            tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
            tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        i = i + 1
        sheet.write(i, 0, "Aktiva Tidak Lancar", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non-current Assets')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period = tot_cur_period + obj.cur_period
            tot_prev_period = tot_prev_period + obj.prev_period
            tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
            tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        i = i + 1
        sheet.write(i, 0, "Piutang", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Receivable')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period = tot_cur_period + obj.cur_period
            tot_prev_period = tot_prev_period + obj.prev_period
            tot_ori_cur_period = tot_ori_cur_period + obj.ori_cur_period
            tot_ori_prev_period = tot_ori_prev_period + obj.prev_period

        i=i+1
        sheet.write(i, 0,'Total Aktiva', format1)
        # sheet.write(i, 1, obj.name, format2)
        sheet.write(i, 2, tot_cur_period, format2)
        sheet.write(i, 3, tot_prev_period, format2)
        # sheet.write(i, 4, obj.currency, format2)
        # sheet.write(i, 5, obj.ori_cur_period, format2)
        # sheet.write(i, 6, obj.ori_prev_period, format2)

        i = i + 2
        sheet.write(i, 0, "Hutang", format1)
        tot_cur_period_hutang = 0
        tot_prev_period_hutang = 0
        i = i + 1
        sheet.write(i, 0, "Hutang Jangka Panjang", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Non-current Liabilities')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_hutang = tot_cur_period_hutang + obj.cur_period
            tot_prev_period_hutang = tot_prev_period_hutang + obj.prev_period

        i = i + 1
        sheet.write(i, 0, "Hutang Lancar", format1)
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Liabilities')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_hutang = tot_cur_period_hutang + obj.cur_period
            tot_prev_period_hutang = tot_prev_period_hutang + obj.prev_period

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Payable')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_hutang = tot_cur_period_hutang + obj.cur_period
            tot_prev_period_hutang = tot_prev_period_hutang + obj.prev_period

        i = i + 1
        sheet.write(i, 0, 'Total Hutang', format1)
        # sheet.write(i, 1, obj.name, format2)
        sheet.write(i, 2, tot_cur_period_hutang, format2)
        sheet.write(i, 3, tot_prev_period_hutang, format2)

        i = i + 2
        sheet.write(i, 0, "Modal", format1)
        tot_cur_period_modal = 0
        tot_prev_period_modal = 0
        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Current Year Earnings')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_modal = tot_cur_period_modal + obj.cur_period
            tot_prev_period_modal = tot_prev_period_modal + obj.prev_period

        lines = self.env['pr.balance_sheet'].search([('account_type', '=', 'Equity')])
        for obj in lines:
            i = i + 1
            sheet.write(i, 0, obj.code, format2)
            sheet.write(i, 1, obj.name, format2)
            sheet.write(i, 2, obj.cur_period, format2)
            sheet.write(i, 3, obj.prev_period, format2)
            sheet.write(i, 4, obj.currency, format2)
            sheet.write(i, 5, obj.ori_cur_period, format2)
            sheet.write(i, 6, obj.ori_prev_period, format2)
            tot_cur_period_modal = tot_cur_period_modal + obj.cur_period
            tot_prev_period_modal = tot_prev_period_modal + obj.prev_period

        i = i + 1
        sheet.write(i, 0, 'Total Modal', format1)
        # sheet.write(i, 1, obj.name, format2)
        sheet.write(i, 2, tot_cur_period_modal, format2)
        sheet.write(i, 3, tot_prev_period_modal, format2)

        i = i + 1
        sheet.write(i, 0, 'Total Hutang dan Modal', format1)
        # sheet.write(i, 1, obj.name, format2)
        sheet.write(i, 2, tot_cur_period_modal+tot_cur_period_hutang, format2)
        sheet.write(i, 3, tot_prev_period_modal+tot_prev_period_hutang, format2)



