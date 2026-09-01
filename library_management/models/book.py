from odoo import api,fields,models

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _rec_name = 'book_name'

    book_name = fields.Char('Book Name')
    book_code = fields.Char('Code',readonly=True,)
    isbn = fields.Char('ISBN')
    author = fields.Char('Author')
    published_date = fields.Date('Published Date')
    price = fields.Float('Price')
    available_copies = fields.Integer('Available Copies')
    description = fields.Text('Description')
    image = fields.Image('Book Image')
    active =fields.Boolean('Active',default=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('available','Available'),
        ('borrowed','Borrowed'),
    ],string='Status',default='draft')


    # Relation 
    category_id = fields.Many2one('library.category',string='Category')
    author_ids = fields.Many2many('library.author',string='Authors')



    def action_available(self):
       for rec in self:
            if rec.book_code == 'New' or not rec.book_code:
               rec.book_code = self.env['ir.sequence'].next_by_code('book.code') or '/'
            rec.state = 'available'

    