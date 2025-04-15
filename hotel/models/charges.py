# -*- coding: utf-8 -*-

# charges.py
from odoo import models, fields, api

class Charges(models.Model):
    _name = 'hotel.charges'
    _description = 'Hotel Charges Master List'

    name = fields.Char("Charge Name")
    description = fields.Char("Charge Description")