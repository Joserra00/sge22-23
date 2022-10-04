# -*- coding: utf-8 -*-

from odoo import models, fields, api


class runescape(models.Model):
    _name = 'runescape.player'
    _description = 'Player of the game'

    name = fields.Char(required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 200, max_height=200)


