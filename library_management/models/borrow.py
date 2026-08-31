from odoo import api,fields,models

class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Borrow'

    name = fields.Char('Reference')
    member_id = fields.Many2one('res.partner',string='Member')
    book_id = fields.Many2one('library.book',string='Book')
    borrow_date = fields.Date('Borrow Date')
    due_date = fields.Date('Due Date')
    active = fields.Boolean('Active',default=True)


