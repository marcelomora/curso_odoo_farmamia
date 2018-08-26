# -*- coding: utf-8 -*-

from openerp import models, fields

class Partner(models.Model):
    _inherit = 'res.partner'

    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        string="Published Books")
