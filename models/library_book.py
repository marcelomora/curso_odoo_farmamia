# -*- coding: utf-8 -*-

from openerp import models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',
        string='Authors')
    short_name = fields.Char('Short Title')

    def name_get(self):
        result = []
        for record in self:
            result.append(record.id, "{} ({})".format(
                record.name, record.date_released)
        return result

