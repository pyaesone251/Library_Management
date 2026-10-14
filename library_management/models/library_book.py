from odoo import models,fields,api
from odoo.exceptions import UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name =fields.Char('Book Name')
    author = fields.Char('Author')
    price = fields.Float('Price')
    category_id = fields.Many2one('library.category')

    def action_search(self):
        self.ensure_one()

        if not self.category_id:
            raise UserError("Please select a category first.")

        books = self.env['library.book'].search([
            ('category_id','=',self.category_id.id)
        ])
        return{
            'type':'ir.actions.act_window',
            'name' : 'Search Books',
            'res_model':'library.book',
            'view_mode':'list,form',
            'domain':[('id','in',books.ids)],
            'target':'current',
        }

    def action_write(self):
        self.ensure_one()
        self.write({
            'price':self.price +1000.00
        })
