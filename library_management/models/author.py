from odoo import api,fields,models

class LibraryAuthor(models.Model):
    _name = 'library.author'
    _description = 'Authors'

    name = fields.Char('Author Name')
    email = fields.Char('Email')
    description = fields.Text('Description')
    image = fields.Image('Image')