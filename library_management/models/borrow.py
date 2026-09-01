from odoo import api,fields,models
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class LibraryBorrow(models.Model):
    _name = 'library.borrow'
    _description = 'Borrow'

    name = fields.Char('Reference',readonly=True)
    member_id = fields.Many2one('res.partner',string='Member')
    member_code_id = fields.Char(related='member_id.member_code',string='Member Code',readonly=True)
    book_id = fields.Many2one('library.book',string='Book')
    borrow_date = fields.Date('Borrow Date',default=fields.Date.context_today)
    due_date = fields.Date('Due Date')
    active = fields.Boolean('Active',default=True)

    state = fields.Selection([
        ('draft','Draft'),
        ('borrowed','Borrowed'),
        ('returned','Returned'),
    ],string='Status',default='draft')

    @api.onchange('borrow_date')
    def _onchange_borrow_date(self):
        if self.borrow_date:
            self.due_date = self.borrow_date + timedelta(days=7)

    def action_borrow(self):
        for rec in self:
            if rec.book_id.available_copies <= 0:
                raise ValidationError("Out of Stock!")
            if rec.name == 'New' or not rec.name:
                rec.name = self.env['ir.sequence'].next_by_code('borrow.code') or '/'
            rec.book_id.available_copies -= 1
            if rec.book_id.available_copies == 0:
                rec.book_id.state = 'borrowed'

        rec.state = 'borrowed'

    def action_returned(self):
        for rec in self:
            rec.book_id.available_copies += 1

            if  rec.book_id.available_copies > 0:
                rec.book_id.state = 'available'

        rec.state = 'returned'



