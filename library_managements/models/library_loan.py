from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class LibraryLoan(models.Model):
    _name = 'library.loan'
    _description = 'Library Loan'
    _order = 'id desc'

    name = fields.Char('Loan Number', required=True)
    book_id = fields.Many2one(
        'library.book', string='Book', required=True, ondelete='restrict',
    )
    member_id = fields.Many2one(
        'library.member', string='Member', required=True, ondelete='restrict',
    )
    due_date = fields.Date('Due Date', required=True)
    borrow_date = fields.Date('Borrow Date', readonly=True, copy=False)
    return_date = fields.Date('Return Date', readonly=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True,
        readonly=True, copy=False)

    # New loans must start in Draft.
    @api.model_create_multi
    def create(self, vals_list):
        new_vals_list = []
        for vals in vals_list:
            vals = dict(vals)
            if vals.get('state', 'draft') != 'draft':
                raise UserError('New loans must start in Draft.')

            if vals.get('borrow_date') or vals.get('return_date'):
                raise UserError('Use the Borrow and Return buttons to set dates.')

            vals['state'] = 'draft'
            vals['borrow_date'] = False
            vals['return_date'] = False
            new_vals_list.append(vals)

        return super().create(new_vals_list)

    # Keep the same rules when records are changed through the ORM.
    def write(self, vals):
        vals = dict(vals)

        if 'borrow_date' in vals or 'return_date' in vals:
            raise UserError('Borrow and return dates are filled automatically.')

        for field_name in ['name', 'book_id', 'member_id', 'due_date']:
            if field_name in vals:
                if 'state' in vals:
                    raise UserError('Save your changes before changing the status.')

                for loan in self:
                    if loan.state != 'draft':
                        raise UserError('Only Draft loans can be edited.')

        if 'state' in vals:
            new_state = vals['state']
            today = fields.Date.context_today(self)

            for loan in self:
                if new_state == 'borrowed':
                    if loan.state != 'draft':
                        raise UserError('Only Draft loans can be borrowed.')

                    if not loan.book_id or not loan.member_id or not loan.due_date:
                        raise UserError('Select a book, member and due date first.')

                    if not loan.member_id.active:
                        raise UserError('Inactive members cannot borrow books.')

                    if loan.due_date < today:
                        raise UserError('The due date cannot be before today.')

                    borrowed_loans = self.env['library.loan'].search([
                        ('book_id', '=', loan.book_id.id),
                        ('state', '=', 'borrowed'),
                    ], limit=1)

                    if borrowed_loans:
                        raise UserError('This book is already borrowed.')

                elif new_state == 'returned':
                    if loan.state != 'borrowed':
                        raise UserError('Only Borrowed loans can be returned.')

                elif new_state == 'cancelled':
                    if loan.state != 'draft':
                        raise UserError('Only Draft loans can be cancelled.')

                else:
                    raise UserError('This status change is not allowed.')

            if new_state == 'borrowed':
                # mapped() returns each different book only once.
                books = self.mapped('book_id')
                if len(books) != len(self):
                    raise UserError('Two loans cannot borrow the same book together.')

                vals['borrow_date'] = today
                vals['return_date'] = False

            elif new_state == 'returned':
                vals['return_date'] = today

        return super().write(vals)

    @api.constrains('due_date', 'borrow_date', 'return_date')
    def _check_dates(self):
        for loan in self:
            if loan.borrow_date and loan.due_date:
                if loan.due_date < loan.borrow_date:
                    raise ValidationError('The due date cannot be before the borrow date.')

            if loan.return_date and loan.borrow_date:
                if loan.return_date < loan.borrow_date:
                    raise ValidationError('The return date cannot be before the borrow date.')

    @api.ondelete(at_uninstall=False)
    def _unlink_except_draft(self):
        for loan in self:
            if loan.state != 'draft':
                raise UserError('Only Draft loans can be deleted.')

    def action_borrow(self):
        self.ensure_one()
        self.write({'state': 'borrowed'})
        return True

    def action_return(self):
        self.ensure_one()
        self.write({'state': 'returned'})
        return True

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'cancelled'})
        return True
