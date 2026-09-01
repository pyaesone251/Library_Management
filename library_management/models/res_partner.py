from odoo import api,fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean('Is Library Member')
    member_code =fields.Char('Member Code',readonly=True)
    membership_date =fields.Date('Membership Date',default=fields.Date.context_today)

    @api.model_create_multi
    def create(self,val_list):
        for vals in val_list:
            vals['member_code'] = self.env['ir.sequence'].next_by_code('res.partner') or '/'
            res = super().create(val_list)
        return res



