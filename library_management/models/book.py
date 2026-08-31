from odoo import api,fields,models

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    book_name = fields.Char('Book Name')
    isbn = fields.Char('ISBN')
    author = fields.Char('Author')
    published_date = fields.Date('Published Date')
    price = fields.Float('Price')
    available_copies = fields.Integer('Available Copies')
    description = fields.Text('Description')
    image = fields.Image('Book Image')
    active =fields.Boolean('Active',default=True)


    # Relation 
    category_id = fields.Many2one('library.category',string='Category')
    author_ids = fields.Many2many('library.author',string='Authors')

    def action_available(self):
        self.state = 'available'