#Guest Registration Model
# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date

class GuestRegistration(models.Model):
    _name = 'hotel.guestregistration'
    _description = 'Hotel guest registration list'

    room_id = fields.Many2one("hotel.rooms", string="Room No.")
    guest_id = fields.Many2one("hotel.guests", string="Guest Name")

    roomname = fields.Char("Room No.", related='room_id.name', store=True)
    roomtname = fields.Char("Room Type", related='room_id.roomtype_id.name', store=True)  # assumes roomtype_id is Many2one
    guestname = fields.Char("Guest Name", related='guest_id.name', store=True)

    datecreated = fields.Date("Date Created", default=fields.Date.context_today)
    datefromSched = fields.Date("Scheduled Check In")
    datetoSched = fields.Date("Scheduled Check Out")
    datefromAct = fields.Date("Actual Check In")
    datetoAct = fields.Date("Actual Check Out")

    state = fields.Selection([
        ('DRAFT', 'Draft'),
        ('RESERVED', 'Reserved'),
        ('CHECKEDIN', 'Checked In'),
        ('CHECKEDOUT', 'Checked Out'),
        ('CANCELLED', 'Cancelled')
    ], string='Status', default='DRAFT')

    name = fields.Char("Guest Registration", compute='_compute_name', store=False)

    @api.depends('room_id.name', 'guest_id.name')
    def _compute_name(self):
        for rec in self:
            room = rec.room_id.name or ''
            guest = rec.guest_id.name or ''
            rec.name = f"{room}, {guest}"
    
    def action_reserve(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid guest.')
            elif not rec.roomname:
                raise ValidationError('Please supply a valid Room Number.')
            elif not rec.datefromSched:
                raise ValidationError('Please supply a valid Date From Schedule.')
            elif not rec.datetoSched:
                raise ValidationError('Please supply a valid Date To Schedule.')
            elif rec.datetoSched < rec.datefromSched:
                raise ValidationError('Invalid Date Range.')
            else:
                self.env.cr.execute("SELECT * FROM public.fncheck_registrationconflict(%s)", (rec.id,))
                result = self.env.cr.fetchone()
                result_cnt = result[0]
                result_msg = result[1]

                if result_cnt == 0:
                    rec.state = "RESERVED"
                else:
                    raise ValidationError(result_msg)

    def action_checkin(self):
        for rec in self:
            if not rec.guest_id:
                raise ValidationError('Please supply a valid guest.')
            elif not rec.room_id:
                raise ValidationError('Please supply a valid Room Number.')
            elif not rec.datefromSched:
                raise ValidationError('Please supply a valid Date From Schedule.')
            elif not rec.datetoSched:
                raise ValidationError('Please supply a valid Date To Schedule.')
            elif rec.datetoSched < rec.datefromSched:
                raise ValidationError('Invalid Date Range.')
            else:
                self.env.cr.execute("SELECT * FROM public.fncheck_registrationconflict(%s)", (rec.id,))
                result = self.env.cr.fetchone()
                result_cnt = result[0]
                result_msg = result[1]

                if result_cnt == 0:
                    rec.state = "CHECKEDIN"
                    rec.datefromAct = date.today()
                else:
                    raise ValidationError(result_msg)

    def action_checkout(self):
        for rec in self:
            if rec.state == "CHECKEDIN":
                rec.state = "CHECKEDOUT"
                rec.datetoAct = date.today()
            else:
                raise ValidationError("Guest is not CHECKED IN.")

    def action_cancel(self):
        for rec in self:
            if rec.state == "CHECKEDIN":
                raise ValidationError("Guest has already CHECKED IN.")
            else:
                rec.state = "CANCELLED"