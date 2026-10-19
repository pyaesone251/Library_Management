from odoo import models,fields,api

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
                'message':f'Book count {count}',
                'type':'info',
                'sicky':False,
            }
        }

    def action_increase_all_price(self):
        self.ensure_one()
        for book in self.book_ids:
            book.write({
                'price':book.price +1000
            })

    def action_filter(self):
        self.ensure_one()
        prices = self.book_ids.filtered(
            lambda p : p.price < 5000
        )
        for price in prices:
            price.write({
                'price': price.price + 200
            })


    def action_show_name(self):
        self.ensure_one()
        books = self.book_ids.filtered(
            lambda b : b.price < 5000
        )

        name = books.mapped('name')
        message = ', '.join(name) if name else 'No name'
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params' : {
                'title': 'Price under 5000',
                'message' : message,
                'type' : 'info',
                'sticky' : False,
            }
        }

    def action_sort_book_price(self):
        self.ensure_one()
        bps = self.book_ids.sorted(
            key = lambda p : p.price
        )
        lines = []
        for bp in bps:
            lines.append(
                f'{bp.name} / {bp.price}'
            )

        message = '\n '.join(lines) if lines else 'No Price'
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'title' : 'Sort by price',
                'message' : message,
                'type' : 'info',
                'sticky' : True,
            }
        }

    def action_sort(self):
        self.ensure_one()
        prices = self.book_ids.filtered(
            lambda pri : pri.price < 5000
        ).sorted(key= lambda p : p.price,reverse=True)

        lines = []
        for price in prices:
            lines.append(
                f'{price.name} ~ {price.price}'
            )

        mess = '\n '.join(lines) if lines else 'No price'
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'title':'Sort by price',
                'message':mess,
                'type':'info',
                'sticky':True,
            }
        }

        

