from odoo import api,models,fields

class LibraryBookCategory(models.Model):
    _name = 'library.category'
    _description = 'Library Category'

    name = fields.Char('Category Name')
    code = fields.Char('Category Code')
    shelf_location = fields.Char('Shelf Location')
    description = fields.Text('Description')
    active =fields.Boolean('Active',default=True)
    color = fields.Integer('Color')
