from odoo import models, fields, api
from odoo.exceptions import UserError


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'name, id'

    # Each record represents one physical book that can be lent out.
    name = fields.Char(string='Book Name', required=True)
    loan_ids = fields.One2many(
        'library.loan', 'book_id', string='Borrowing History', readonly=True,
    )
    is_available = fields.Boolean(
        string='Available',
        compute='_compute_is_available',
        store=True,
    )

    @api.depends('loan_ids.state')
    def _compute_is_available(self):
        for book in self:
            borrowed_loans = book.loan_ids.filtered(
                lambda loan: loan.state == 'borrowed'
            )
            if borrowed_loans:
                book.is_available = False
            else:
                book.is_available = True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_has_loans(self):
        for book in self:
            if book.loan_ids:
                raise UserError('A book with borrowing history cannot be deleted.')
