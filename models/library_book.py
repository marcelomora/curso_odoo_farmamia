# -*- coding: utf-8 -*-

from openerp import models, fields, api, _
from openerp.fields import Date as fDate
from datetime import timedelta as td
from openerp.exceptions import UserError

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.archive = not record.archive

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['base.archive']
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'

    name = fields.Char('Title', required=True)
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',
        string='Authors')
    short_name = fields.Char('Short Title', size=100, translate=False)

    notes = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')],
        'State')
    description = fields.Html('Description')
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_updated = fields.Datetime('Last Updated')
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher')
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'cancel': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
   )

    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4), # Optional precision (total, decimals),
    )

    age_days = fields.Float(
        string = 'Days since release',
        compute = '_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False,
    )


    manager_remarks = fields.Text("Manager Remarks")
    is_magazine = fields.Boolean("Magazine")
    isbn = fields.Char("ISBN")

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique')
    ]

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError(
                    'Release date must be in the past')

    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = fDate.from_string(book.date_release) - today
            book.age_days = -delta.days

    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = today - td(days=book.age_days)
            book.date_release = fDate.to_string(d)


    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]




    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(
                record.name, record.date_release)))
        return result

    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return(old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                raise UserError(_("State change not allowed"))

    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])


    @api.model
    def create_end_customer(self):
        vals = {
            'name': u'Consumidor Final',
            'vat': 'EC9999999999',
            'email': 'facturacionelectronica@farmamia.com',
            'is_company': False
        }

        record = self.env['res.partner'].create(vals)

    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if not self.user_has_groups('my_module.group_library_manager'):
            if 'manager_remarks' in values:
                raise UserError(_("You are not allowed to modify 'manager remarks'"))
        return super(LibraryBook, self).create(values)

    @api.multi
    def write(self, values):
        if not self.user_has_groups('my_module.group_library_manager'):
            if 'manager_remarks' in values:
                raise UserError(_("You are not allowed to modify 'manager remarks'"))
        return super(LibraryBook, self).write(values)
