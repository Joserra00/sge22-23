# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'runescape.player'
    _description = 'Player of the game'

    name = fields.Char(required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 200, max_height=200)
    armor = fields.Many2one('runescape.armor')
    coins = fields.Integer(default=0)
    sword = fields.Many2one('runescape.sword')



class armor(models.Model):
    _name = 'runescape.armor'
    _description = 'Runescape armor'

    material=fields.Selection([('1','Iron'),('2','Mithril'),('3','Rune')])
    defense=fields.Integer()

class sword(models.Model):
    _name = 'runescape.sword'
    _description = 'Runescape sword'

    material=fields.Selection([('1','Iron'),('2','Mithril'),('3','Rune')])
    damage=fields.Integer()


class material(models.Model):
    _name = 'runescape.material'
    _description = 'Runescape material'

    type=fields.Selection([('1','Iron'),('2','Mithril'),('3','Rune')])

