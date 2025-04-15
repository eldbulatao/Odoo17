# -*- coding: utf-8 -*-

# roomtypes.py
from odoo import models, fields, api

class Roomtypes(models.Model):
    _name = 'hotel.roomtypes'
    _description = 'Hotel roomtypes master list'
    _order = "name"

    name = fields.Char("Roomtype Name")
    description = fields.Char("Roomtype Description")

    photo_bed = fields.Image("Bed Photo")
    photo_restroom = fields.Image("Restroom Photo")

    room_ids=fields.One2many('hotel.rooms','roomtype_id',string='Rooms')