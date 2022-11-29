# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

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
    sword = fields.Many2one('runescape.sword',readonly=True)
    swordBuy = fields.Many2one('runescape.sword',default=_first_sword)
    swordBuy_image = fields.Image(related='swordBuy.sword_image')
    swordBuy_price = fields.Integer(related='swordBuy.price')
    damage = fields.Integer(related='sword.damage')
    sword_image = fields.Image(related='sword.sword_image')
    sword_price = fields.Integer(related='sword.price')

    def _first_armor(self):
        return self.env['runescape.armor'].search([])[6]
    armor = fields.Many2one('runescape.armor',readonly=True)
    armorBuy = fields.Many2one('runescape.armor',default=_first_armor)
    armorBuy_image = fields.Image(related='armorBuy.armor_image')
    armorBuy_price = fields.Integer(related='armorBuy.price')
    defense = fields.Integer(related='armor.defense')
    armor_image=fields.Image(related='armor.armor_image')
    armor_price = fields.Integer(related='armor.price')
    strength = fields.Integer(default=5)
    travel = fields.One2many('runescape.travel_dungeon', 'player')
    travel_name = fields.Char(compute='_location_assign')
    travel_type = fields.Char(compute='_location_assign')

    @api.model
    def create(self, values):
        new_id = super(player, self).create(values)
        self.env['runescape.travel_dungeon'].create(
            {'player': new_id.id, 'travel_to': '1', 'zone': self.env['runescape.zone'].search([])[0].id})
        return new_id

    def _location_assign(self):
        for player in self:
            variable = player.travel
            length = (len(variable)-1)
            if len(variable[length].dungeon)>0:
                player.travel_name=variable[length].dungeon.name
            else:
                player.travel_name=variable[length].zone.name
            if variable[length].travel_to=='1':
                player.travel_type = "City"
            else:
                player.travel_type = "Dungeon"    



    #@api.constrains('city')
    #def _player_location(self):
    #    for s in self:
     #       if len(self.city)>0 and len(self.dungeon)>0:
      #          raise ValidationError("No puedes estar en una zona segura y una Dungeon a la vez")
 
  

 


    @api.constrains('hp')
    def _player_hp(self):
        for s in self:
            if self.hp > 100 or self.hp<0:
                raise ValidationError("El maximo de vida es 100 y el minimo 0")

    def buy_sword(self):
        for s in self:
            resultado=(s.coins-s.swordBuy_price)
            if resultado<0:
                print("No hay suficientes coins")

            else:
                s.coins=resultado
                s.sword=s.swordBuy.id
                s.swordBuy=False


    def buy_armor(self):
        for s in self:
            resultado = (s.coins-s.armorBuy_price)
            if resultado < 0:
                print("No hay suficientes coins")

            else:
                s.coins = resultado
                s.armor = s.armorBuy.id
                s.armorBuy = False


   



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
    health_gain=fields.Integer()

class dungeon(models.Model):
    _name = 'runescape.dungeon'
    _description = 'Runescape dungeon'

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
    


class travel_dungeon(models.Model):
    _name = 'runescape.travel_dungeon'
    _description = 'Runescape travel'

    player = fields.Many2one('runescape.player',ondelete='cascade')
    travel_to=fields.Selection([('1','City'),('2','Dungeon')])
    dungeon = fields.Many2one('runescape.dungeon')
    zone = fields.Many2one('runescape.zone')
    date_start = fields.Datetime(readonly=True, default = fields.Datetime.now)
    date_end = fields.Datetime(compute='_get_time')  # Calcul de dates
    mob = fields.One2many(related='dungeon.mob')

    def _get_time(self):
        for s in self:
            s.date_end = fields.Datetime.to_string(fields.Datetime.from_string(s.date_start) + timedelta(minutes=1))
    def battle_mob(self):
        for s in self:
            print(s.dungeon.mob.qty)

