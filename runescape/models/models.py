# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
    _name = 'runescape.player'
    _description = 'Player of the game'

    name = fields.Char(required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 200, max_height=200)
    coins = fields.Integer(default=20000)
    hp = fields.Integer(default=20)
    sword = fields.Many2one('runescape.sword')
    damage = fields.Integer(related='sword.damage')
    sword_image = fields.Image(related='sword.sword_image')
    armor = fields.Many2one('runescape.armor')
    defense = fields.Integer(related='armor.defense')
    armor_image=fields.Image(related='armor.armor_image')
    strength = fields.Integer(default=1)
    city = fields.Many2one('runescape.zone')




class armor(models.Model):
    _name = 'runescape.armor'
    _description = 'Runescape armor'

    material=fields.Selection([('1','Bronze'),('2','Iron'),('3','Steel'),('4','Black'),('5','Mithril'),('6','Adamant'),('7','Rune')])
    defense=fields.Integer()
    price = fields.Integer()
    name = fields.Char()
    armor_image = fields.Image(max_width=100, max_height=100)

class sword(models.Model):
    _name = 'runescape.sword'
    _description = 'Runescape sword'

    material=fields.Selection([('1','Bronze'),('2','Iron'),('3','Steel'),('4','Black'),('5','Mithril'),('6','Adamant'),('7','Rune')])
    damage=fields.Integer()
    price = fields.Integer()
    name = fields.Char()
    sword_image = fields.Image(max_width=50, max_height=50)

class zone(models.Model):
    _name = 'runescape.zone'
    _description = 'Runescape city'

    name = fields.Char()
    avatar = fields.Image(max_width=50, max_height=50)
    price = fields.Integer()

class dungeon(models.Model):
    _name = 'runescape.dungeon'
    _description = 'Runescape city'

    name = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    price = fields.Integer()

class mob(models.Model):
    _name = 'runescape.mob'
    _description = 'Runescape mob'

    name = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    damage = fields.Integer()
    strength = fields.Integer()
    defense = fields.Integer()
    hp = fields.Integer()




