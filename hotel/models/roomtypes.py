# -*- coding: utf-8 -*-

# roomtypes.py
from odoo import models, fields, api

class roomtypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Hotel roomtypes master list'
    _order = "name"

    name = fields.Char("Room Type Name")
    description = fields.Char("Room Type Description")
    photo_bed = fields.Image("Bed Photo")
    photo_restroom = fields.Image("Restroom Photo")
    dailycharges_ids = fields.One2many('hotel.dailycharges', 'roomtype_id', string='Daily Charges')


class dailycharges(models.Model):
    _name = 'hotel.dailycharges'
    _description = 'Hotel roomtype daily charges list'

    charge_id = fields.Many2one('hotel.charges', string="Charge Title")
    amount = fields.Float("Daily Amount", digits=(10, 2))
    roomtype_id = fields.Many2one('hotel.roomtypes', string="Room Type")