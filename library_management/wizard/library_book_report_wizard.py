import io
import xlsxwriter
import base64
from odoo import api,fields,models,_
from odoo.exceptions import ValidationError

class LibraryBookReportWizard(models.TransientModel):
    _name = 'library.book.report.wizard'
    _description = 'Book Report Wizard'

    start_date = fields.Date('From Date',required=True)
    end_date = fields.Date('To Date',required=True)
    category_id = fields.Many2one('library.category','Category')
    report_file = fields.Binary('Excel File',readonly=True,attachment=False)
    report_filename = fields.Char('FileName',readonly=True)

    def action_export_excel(self):
        self.ensure_one()
        if self.start_date > self.end_date:
            raise ValidationError(_("Start date can't be greater than end date"))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{"in_memory":True})
        worksheet = workbook.add_worksheet("Book Report")

        # Format
        title_format = workbook.add_format({
            'border':1,
            'bold':True,
            'font_size':16,
            'align':'center',
        })

        sub_title_format = workbook.add_format({
            'border':1,
            'font_size':14,
            'align':'center',
        })

        header_format = workbook.add_format({
            'font_size':14,
            'align':'center',
            'border':1,
            'bg_color':"#c4c3c3"
        })

        text_format = workbook.add_format({
            'border':1,
            'align':'center',
        })

        price_format = workbook.add_format({
            'align':'center',
            'border':1,
            'num_format':'#,##0.00',
        })

        # Row & Column 
        worksheet.set_column("A:A",6)
        worksheet.set_column("B:B",12)
        worksheet.set_column("C:C",30)
        worksheet.set_column("D:E",18)
        worksheet.set_column("F:F",10)
        worksheet.set_column("G:G",22)

        current_company = self.env.company
        # worksheet.merge_range("A1:G1",current_company.name,title_format)
        worksheet.merge_range("A1:G1","Book List Reports",title_format)

        books = self.env['library.book'].search([('published_date','>=',self.start_date),('published_date','<=',self.end_date),('category_id','=',self.category_id.id)if self.category_id else (1, '=', 1)])

        # Header
        worksheet.write(1,0,"No",header_format)
        worksheet.write(1,1,"Book Code",header_format)
        worksheet.write(1,2,"Book Name",header_format)
        worksheet.write(1,3,"Category",header_format)
        worksheet.write(1,4,"Author",header_format)
        worksheet.write(1,5,"Price",header_format)
        worksheet.write(1,6,"Available Copies",header_format)

        # Data
        row=2
        for no,book in enumerate(books,start=1):
            authors = ", ".join(book.author_ids.mapped('name')) if book.author_ids else '/'
            worksheet.write(row,0,no,text_format)
            worksheet.write(row,1,book.book_code or '/',text_format)
            worksheet.write(row,2,book.book_name or '/',text_format)
            worksheet.write(row,3,book.category_id.name or '/',text_format)
            worksheet.write(row,4,authors,text_format)
            worksheet.write(row,5,book.price or '/',price_format)
            worksheet.write(row,6,book.available_copies or '/',text_format)
            row += 1


        workbook.close()
        filename = ("book_report"+str(self.start_date)+"_to_"+str(self.end_date))
        excel_data = output.getvalue()
        encode_excel = base64.b64encode(excel_data)
        self.report_file = encode_excel
        self.report_filename = filename

        output.close()
        download_url = ("/web/content/"+self._name+"/"+str(self.id)+"/report_file/"+filename+"?download=true")
        return{
            "type":"ir.actions.act_url",
            "url":download_url,
            "target":"self",
        }
