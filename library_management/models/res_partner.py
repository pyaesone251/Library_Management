from odoo import api,fields,models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_library_member = fields.Boolean('Is Library Member')
    member_code =fields.Char('Member Code')
    membership_date =fields.Date('Membership Date')