from odoo import models, fields, api
from odoo.exceptions import UserError


class LibraryMember(models.Model):
    _name = 'library.member'
    _description = 'Library Member'
    _order = 'name, id'

    name = fields.Char(string='Member Name', required=True)
    phone = fields.Char(string='Phone')
    active = fields.Boolean(default=True)
    loan_ids = fields.One2many(
        'library.loan', 'member_id', string='Borrowing History', readonly=True,
    )
    borrowed_count = fields.Integer(
        string='Books Borrowed', compute='_compute_borrowed_count',
    )

    @api.depends('loan_ids.state')
    def _compute_borrowed_count(self):
        for member in self:
            borrowed_loans = member.loan_ids.filtered(
                lambda loan: loan.state == 'borrowed'
            )
            member.borrowed_count = len(borrowed_loans)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_has_loans(self):
        for member in self:
            if member.loan_ids:
                raise UserError(
                    'A member with borrowing history cannot be deleted. '
                    'Archive the member instead.'
                )
