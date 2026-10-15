from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError

class LibraryCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char('Category Name')
    book_ids = fields.One2many('library.book','category_id',string='Books')

    def action_count(self):
        self.ensure_one()
        count = len(self.book_ids)
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'title':self.name,
                'message':f"Book count {count}",
                'type':'info',
                'sticky':False,
            }
        }

    def action_price(self):
        self.ensure_one()

        for book in self.book_ids:
            if book.price < 2000.00:
                book.write({
                    'price':book.price +500.00,
                })

                