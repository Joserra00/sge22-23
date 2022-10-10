# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'runescape.player'
    _description = 'Player of the game'

    name = fields.Char(required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 200, max_height=200)
    world = fields.Many2one('runescape.world')

class world(models.Model):
    _name = 'runescape.world'
    _description = 'Runescape World'

    name = fields.Char(required=True)
    player = fields.One2many('runescape.player','world')

class armor(models.Model):
    _name = 'runescape.armor'
    _description = 'Runescape armor'


class material (models.Model):
    _name = 'runescape.material'
    _description = 'Runescape material'