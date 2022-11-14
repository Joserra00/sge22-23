# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class player(models.Model):
    _name = 'runescape.player'
    _description = 'Player of the game'

    name = fields.Char(required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 100, max_height=100)
    coins = fields.Integer(default=7000)
    hp = fields.Integer(default=20)
    def _first_sword(self):
        return self.env['runescape.sword'].search([])[6]
    sword = fields.Many2one('runescape.sword',default=_first_sword)
    damage = fields.Integer(related='sword.damage')
    sword_image = fields.Image(related='sword.sword_image')
    sword_price = fields.Integer(related='sword.price')
    def _first_armor(self):
        return self.env['runescape.armor'].search([])[6]

    armor = fields.Many2one('runescape.armor',default=_first_armor)
    defense = fields.Integer(related='armor.defense')
    armor_image=fields.Image(related='armor.armor_image')
    armor_price = fields.Integer(related='armor.price')
    strength = fields.Integer(default=5)
    city = fields.Many2one('runescape.zone')
    dungeon = fields.Many2one('runescape.dungeon')


    @api.constrains('city')
    def _player_location(self):
        for s in self:
            if len(self.city)>0 and len(self.dungeon)>0:
                raise ValidationError("No puedes estar en una zona segura y una Dungeon a la vez")
        # all records passed the test, don't return anything

   






class armor(models.Model):
    _name = 'runescape.armor'
    _description = 'Runescape armor'

    material=fields.Selection([('1','Bronze'),('2','Iron'),('3','Steel'),('4','Black'),('5','Mithril'),('6','Adamant'),('7','Rune')])
    defense=fields.Integer()
    price = fields.Integer()
    name = fields.Char()
    armor_image = fields.Image(max_width=50, max_height=50)

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
    avatar = fields.Image(max_width=100, max_height=100)
    price = fields.Integer()

class dungeon(models.Model):
    _name = 'runescape.dungeon'
    _description = 'Runescape city'

    name = fields.Char()
    avatar = fields.Image(max_width=100, max_height=100)
    price = fields.Integer()
    mob = fields.One2many('runescape.dungeon_mob_rel','dungeon')

class dungeon_mob_rel(models.Model):
    _name = 'runescape.dungeon_mob_rel'
    _description= 'Runescape rel'

    name = fields.Char(related="mob.name")
    dungeon = fields.Many2one("runescape.dungeon")
    mob=fields.Many2one('runescape.mob')
    qty=fields.Integer()


class mob(models.Model):
    _name = 'runescape.mob'
    _description = 'Runescape mob'

    name = fields.Char()
    avatar = fields.Image(max_width=50, max_height=50)
    damage = fields.Integer()
    strength = fields.Integer()
    defense = fields.Integer()
    hp = fields.Integer()
    dungeon = fields.Many2many('runescape.dungeon')




