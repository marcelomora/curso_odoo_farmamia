# -*- coding: utf-8 -*-

from openerp import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string="Published Books")

class LibraryMember(models.Model):
    _inherits = {'res.partner': 'partner_id'}
    _name = 'library.member'

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char("Number")
