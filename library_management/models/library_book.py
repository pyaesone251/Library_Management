from odoo import models,fields,api
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Books'

    name = fields.Char('Book Name')
    author = fields.Char('Author')
    price = fields.Float('Price')
    category_id = fields.Many2one('library.category',string='Category')
    category_name = fields.Char('Category Name',related="category_id.name")

    def action_create_book(self):
        book = self.env['library.book'].create({
            'name':'Practice Book',
            'author':'Practice Author',
            'price':2000,
        })
        return{
            'type':'ir.actions.act_window',
            'name':'Book Create',
            'res_model':'library.book',
            'view_mode':'form',
            'res.id':book.id,
            'target':'current',
        }

    def action_search_same_category(self):
        self.ensure_one()

        if not self.category_id:
            raise UserError('Pls Select Category!')
        
        search_cate = self.env['library.book'].search([
            ('category_id','=',self.category_id.id),
        ])
        return{
            'type':'ir.actions.act_window',
            'name':'Book Category',
            'res_model':'library.book',
            'view_mode':'list',
            'domain' : [('id','in',search_cate.ids)],
            'target':'current',
        }

    def action_search_cheap_book(self):
        self.ensure_one()


        cheap_price = self.env['library.book'].search([
            ('price','<',5000)
        ])
        return{
            'type':'ir.actions.act_window',
            'name':'Price Cheap',
            'res_model':'library.book',
            'view_mode':'list',
            'domain':[('id','in',cheap_price.ids)],
            'target':'current',
        }

    def action_increase_price(self):
        self.ensure_one()
        self.write({
            'price':self.price +300,
        })

    def action_move_to_history(self):
        self.ensure_one()

        history_category = self.env['library.category'].search([
            ('name','=','History')
        ],limit=1)

        if not self.category_id:
            raise UserError("Pls,check your category")

        self.write({
            'category_id': history_category.id,
        })

    def action_delete_book(self):
        self.ensure_one()
        self.unlink()
        return{
            'type':'ir.actions.act_window',
            'name':'Book Delete',
            'res_model':'library.book',
            'view_mode':'list'
        }

    @api.constrains('price')
    def _check_price(self):
        for book in self:
            if float_compare(book.price,0.0,precision_digits=0) < 0:
                raise ValidationError(
                    'Book price cannot be negative'
                )




        