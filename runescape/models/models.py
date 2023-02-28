# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from typing import Final
from random import *
WOLF_QTY: Final[int] = 15
class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _description = 'Player of the game'

    #name = fields.Char(required=True)
    password = fields.Char()
    avatar = fields.Image(max_width = 100, max_height=100)
    coins = fields.Integer(default=7000)
    hp = fields.Integer(default=20)
    is_player = fields.Boolean(default=False)

    def _first_sword(self):
        return self.env['runescape.sword'].search([])[6]

    sword = fields.Many2one('runescape.sword',readonly=True)
    swordBuy = fields.Many2one('runescape.sword'#,default=_first_sword,domain="[('id','!=',sword)]"
    )
    swordBuy_image = fields.Image(related='swordBuy.sword_image')
    swordBuy_price = fields.Integer(related='swordBuy.price')
    damage = fields.Integer(related='sword.damage')
    sword_image = fields.Image(related='sword.sword_image')
    sword_price = fields.Integer(related='sword.price')

    def _first_armor(self):
        return self.env['runescape.armor'].search([])[6]

    armor = fields.Many2one('runescape.armor',readonly=True)
    armorBuy = fields.Many2one('runescape.armor'#,default=_first_armor,domain="[('id','!=',armor)]"
    )
    armorBuy_image = fields.Image(related='armorBuy.armor_image')
    armorBuy_price = fields.Integer(related='armorBuy.price')
    defense = fields.Integer(related='armor.defense')
    armor_image=fields.Image(related='armor.armor_image')
    armor_price = fields.Integer(related='armor.price')
    money_after_buy = fields.Integer(readonly=True,compute='_set_money_buy')
    strength = fields.Integer(default=5)
    travel = fields.One2many('runescape.travel_dungeon', 'player',ondelete='cascade')
    travel_name = fields.Char(compute='_location_assign')
    travel_type = fields.Char(compute='_location_assign')

    def aumentar_strength(self):
        for s in self:
            lvl = (s.strength + 1)

            s.write({'strength': lvl})

    def disminuir_strength(self):
        for s in self:
            lvl = (s.strength - 1)

            s.write({'strength': lvl})


    @api.model
    def create(self, values):
        new_id = super(player, self).create(values)
        self.env['runescape.travel_dungeon'].create(
            {'player': new_id.id, 'travel_to': '1', 'zone': self.env['runescape.zone'].search([])[0].id})
        if not self.armor:
            raise ValidationError("Debes elegir tu armadura y tu sword")
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


    @api.onchange('armorBuy','swordBuy')
    def _set_money_buy(self):
        for s in self:
                s.money_after_buy=(s.coins-(s.armorBuy_price+s.swordBuy_price))

 


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
                s.swordBuy=False
            else:
                s.write({'coins':resultado,
                            'sword':s.swordBuy,
                            'swordBuy':False,
                            'money_after_buy':s.coins-s.swordBuy_price})

            
                


    def buy_armor(self):
        for s in self:
            resultado = (s.coins-s.armorBuy_price)
            if resultado < 0:
                print("No hay suficientes coins")
                s.armorBuy=False

            else:
                 s.write({'coins':resultado,
                            'armor':s.armorBuy,
                            'armorBuy':False,
                            'money_after_buy':s.coins-s.armorBuy_price})

    def generate_travel(self):
        
        return {
        'type': 'ir.actions.act_window',
        'res_model': 'runescape.travel_wizard',
        'context': {'player_id': self.id},
        'view_mode': 'form',
        'view_type': 'form',    
        'target': 'new', 
    }
    def generate_battle(self):
            return {
        'type': 'ir.actions.act_window',
        'res_model': 'runescape.battle_wizard',
        'context': {'player_id': self.id},
        'view_mode': 'form',
        'view_type': 'form',    
        'target': 'new', 
    }

   



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

    @api.model
    def respawn_mobs(self):
        mob_rel=self.env['runescape.dungeon_mob_rel'].search([])
        for s in mob_rel:
            s.qty=randrange(8, 20, 2) 
            print(s.qty)


class mob(models.Model):
    _name = 'runescape.mob'
    _description = 'Runescape mob'

    name = fields.Char()
    avatar = fields.Image(max_width=50, max_height=50)
    damage = fields.Integer()
    strength = fields.Integer()
    defense = fields.Integer()
    hp = fields.Integer()
    gold_gain_bykill = fields.Integer()
    


class travel_dungeon(models.Model):
    _name = 'runescape.travel_dungeon'
    _description = 'Runescape travel'

    player = fields.Many2one('res.partner',domain="[('is_player','=',True)]",ondelete='cascade')
    travel_to=fields.Selection([('1','City'),('2','Dungeon')],default='1')
    dungeon = fields.Many2one('runescape.dungeon')
    zone = fields.Many2one('runescape.zone')
    date_start = fields.Datetime(readonly=True, default = fields.Datetime.now())
    date_end = fields.Datetime()
    mob = fields.One2many(related='dungeon.mob')
    price = fields.Integer(compute='_get_price')

    @api.model
    def create(self, values):
        new_id = super(travel_dungeon, self).create(values)
        new_id.player.coins -= new_id.price
        return new_id

    @api.onchange('dungeon','zone')
    def _get_price(self):
        for s in self:
            if len(s.dungeon)>0:
                s.price=s.dungeon.price
            if len(s.zone)>0:
                s.price=s.zone.price

    @api.constrains('player')
    def _enough_money(self):
        for s in self:
            if s.player.coins<s.price:
                raise ValidationError("No tienes suficientes coins para realizar el viaje")
            else:
                s.player.coins-s.price   

    def battle_mob(self):
        for s in self:
            mob_health= s.mob.mob.hp
            player_health= s.player.hp
            if(s.dungeon.mob.qty==0):
                raise ValidationError("No quedan mobs en la dungeon")
            
            while mob_health>0 and player_health>0:
                damage_dealt_mob=(randrange(0,int(s.dungeon.mob.mob.damage*s.dungeon.mob.mob.strength/s.player.defense),1))
                player_health -=damage_dealt_mob
                damage_dealt_mob_str = "Damage by mob: "+str(damage_dealt_mob)+", Player remaining hp : "+str(player_health)

                damage_dealt_player = ( randrange(0, int(s.player.strength*s.player.damage/s.dungeon.mob.mob.defense), 1))
                mob_health -=damage_dealt_player
                damage_dealt_player_str ="Damage by player: "+str(damage_dealt_player)+", Mob remaining hp : "+str(mob_health)

                print(damage_dealt_mob_str)
                print(damage_dealt_player_str)

            if player_health>0:
                s.player.coins+=s.dungeon.mob.mob.gold_gain_bykill
                s.dungeon.mob.qty-=1
                print(str(s.player.name)+" coins: "+str(s.player.coins))
           
#WIZARD PLAYER
class player_wizard(models.TransientModel):
    _name = 'runescape.player_wizard'
    _description = 'Wizard per crear players'


    name = fields.Char()
    password = fields.Char()
    avatar = fields.Image(max_width=200, max_height=200)
    is_player=fields.Boolean(default=False)

    def create_player(self):
        self.ensure_one()
        self.env['res.partner'].create({
                            'name':self.name,
                            'password': self.password,
                            'avatar': self.avatar,
                            'is_player': True
                         })


class travel_wizard(models.TransientModel):
    _name = 'runescape.travel_wizard'
    _description = 'Wizard per crear travel'
    def _get_player(self):
      return self.env['res.partner'].search([('id',"=",self.env.context.get('player_id'))])
    
    player = fields.Many2one('res.partner',readonly=True,domain="[('is_player','=',True)]",ondelete='cascade',default=_get_player)
    travel_to=fields.Selection([('1','City'),('2','Dungeon')],default='1')
    dungeon = fields.Many2one('runescape.dungeon')
    zone = fields.Many2one('runescape.zone')
    date_start = fields.Datetime(readonly=True, default = fields.Datetime.now)
    date_end = fields.Datetime(readonly=True,compute='_get_time',store=True)
    mob = fields.One2many(related='dungeon.mob')
    price = fields.Integer(compute='_get_price')

   


    @api.onchange('dungeon','zone')
    def _get_price(self):
        for s in self:
            if len(s.dungeon)>0:
                s.price=s.dungeon.price
            if len(s.zone)>0:
                s.price=s.zone.price

    @api.constrains('player')
    def _enough_money(self):
        for s in self:
            if s.player.coins<s.price:
                raise ValidationError("No tienes suficientes coins para realizar el viaje")
            else:
                s.player.coins-s.price


    def _get_time(self):
        for s in self:
            s.date_end = fields.Datetime.to_string(fields.Datetime.from_string(s.date_start) + timedelta(minutes=1))

    def battle_mob(self):
        for s in self:
            mob_health= s.mob.mob.hp
            player_health= s.player.hp
            if(s.dungeon.mob.qty==0):
                raise ValidationError("No quedan mobs en la dungeon")
            
            while mob_health>0 and player_health>0:
                damage_dealt_mob=(randrange(0,int(s.dungeon.mob.mob.damage*s.dungeon.mob.mob.strength/5),1))
                player_health -=damage_dealt_mob
                damage_dealt_mob_str = "Damage by mob: "+str(damage_dealt_mob)+", Player remaining hp : "+str(player_health)

                damage_dealt_player = ( randrange(0, int(s.player.strength*s.player.damage/10), 1))
                mob_health -=damage_dealt_player
                damage_dealt_player_str ="Damage by player: "+str(damage_dealt_player)+", Mob remaining hp : "+str(mob_health)

                print(damage_dealt_mob_str)
                print(damage_dealt_player_str)

            if player_health>0:
                s.player.coins+=s.dungeon.mob.mob.gold_gain_bykill
                s.dungeon.mob.qty-=1
                print(str(s.player.name)+" coins: "+str(s.player.coins))
   

    def launch_travel(self):
        self.ensure_one()
        self.env['runescape.travel_dungeon'].create({
                            'player':self.player.id,
                            'travel_to': self.travel_to,
                            'dungeon': self.dungeon.id,
                            'zone': self.zone.id,
                            'date_start' : self.date_start,
                            'date_end' : self.date_end,
                            'mob' : self.mob,
                            'price' : self.price
                         })

class battle(models.Model):
    _name = 'runescape.battle'
    _description = 'Runescape battle'


    player1 =  fields.Many2one('res.partner',domain="[('is_player','=',True), ('id', '!=', player2)]")
    player1_bet = fields.Integer(default=0)
    player2 =  fields.Many2one('res.partner',domain="[('is_player','=',True), ('id', '!=', player1)]")
    player2_bet = fields.Integer(default=0)
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now)
    state = fields.Selection([('1', 'Player 1'), ('2', 'Player 2'), ('3', 'Launch')], default='1')
    date_end = fields.Datetime()
    battle_ended=fields.Boolean(default=False)
    
    @api.model
    def update_battle(self):
         for s in self.search([('battle_ended',"=",False)]):
            if (s.date_end < fields.Datetime.now()) and not s.battle_ended:
                player1_health = s.player1.hp
                player2_health = s.player2.hp
                if s.player1.defense<1 or s.player2.defense<1:
                       return {
                    'warning': {'title': "Warning", 'message': "Uno de los players no tiene armadura no se puede hacer la batalla", 'type': 'notification'},
                } 

                while player1_health>0 and player2_health>0:
                    damage_dealt_player1=(randrange(0,int(s.player1.damage*s.player1.strength/(s.player1.defense+1)),1))
                    player2_health -=damage_dealt_player1
                    damage_dealt_player1_str = "Damage by "+s.player1.name+": "+str(damage_dealt_player1)+", "+s.player2.name+" remaining hp : "+str(player2_health)

                    damage_dealt_player2 = ( randrange(0, int(s.player2.strength*s.player2.damage/(s.player2.defense+1)), 1))
                    player1_health -=damage_dealt_player2
                    damage_dealt_player2_str ="Damage by "+s.player2.name+": "+str(damage_dealt_player2)+", "+s.player1.name+" remaining hp : "+str(player1_health)

                    print(damage_dealt_player1_str)
                    print(damage_dealt_player2_str)
                if player1_health>0:
                    s.player1.coins+=s.player2_bet
                    print( s.player1.name+" wins, coins gain: "+str(s.player2_bet))
                else:
                    s.player2.coins+=s.player1_bet
                    print(s.player2.name+" wins, coins gain: "+str(s.player1_bet))

                s.battle_ended=True
            else: print("No battles to launch")

    @api.onchange('player1')
    def _funcion(self):
        for s in self:
            player1_qty = self.env['res.partner'].search([('is_player',"=",True)])
            player1_qty = player1_qty.filtered(lambda r: r.id != s.player1.id)
            print(player1_qty)
            #return {'domain':{'player2'[('id','in',player1_qty.ids)]}}


    @api.onchange('player1_bet')
    def _get_player1_stats(self):
        for s in self:
            
            if s.player1.coins<s.player1_bet:
                raise ValidationError("No puedes apostar mas dinero del que tienes")

    @api.onchange('player2_bet')
    def _get_player2_stats(self):
        for s in self:
            if s.player2.coins<s.player2_bet:
                raise ValidationError("No puedes apostar mas dinero del que tienes")

    def launch_battle(self):
        for s in self:
            player1_health = s.player1.hp
            player2_health = s.player2.hp
            while player1_health>0 and player2_health>0:
                damage_dealt_player1=(randrange(0,int(s.player1.damage*s.player1.strength/s.player1.defense),1))
                player2_health -=damage_dealt_player1
                damage_dealt_player1_str = "Damage by Player 1: "+str(damage_dealt_player1)+", Player 2 remaining hp : "+str(player2_health)

                damage_dealt_player2 = ( randrange(0, int(s.player2.strength*s.player2.damage/s.player2.defense), 1))
                player1_health -=damage_dealt_player2
                damage_dealt_player2_str ="Damage by Player 2: "+str(damage_dealt_player2)+", Player 1 remaining hp : "+str(player1_health)

                print(damage_dealt_player1_str)
                print(damage_dealt_player2_str)
            if player1_health>0:
                s.player1.coins+=s.player2_bet
                print("Player 1 wins, coins gain: "+str(s.player2_bet))
            else:
                s.player2.coins+=s.player1_bet
                print("Player 2 wins, coins gain: "+str(s.player1_bet))
            

    def back(self):
        for b in self:
            if b.state == '2':
                b.state = '1'
            if b.state == '3':
                b.state = '2'

    def next(self):
        for b in self:
            if b.state == '2':
                b.state = '3'
            if b.state == '1':
                b.state = '2'

class battle_wizard(models.TransientModel):
    _name = 'runescape.battle_wizard'
    _description = 'Runescape battle wizard'
    def _get_player(self):
        return self.env['res.partner'].search([('id',"=",self.env.context.get('player_id'))])

    player1 =  fields.Many2one('res.partner',domain="[('is_player','=',True), ('id', '!=', player2)]",default=_get_player,readonly=True)
    player1_bet = fields.Integer(default=0)
    player2 =  fields.Many2one('res.partner',domain="[('is_player','=',True), ('id', '!=', player1)]")
    player2_bet = fields.Integer(default=0)
    date_start = fields.Datetime(readonly=True, default=fields.Datetime.now())
    date_end = fields.Datetime(default=fields.Datetime.now())
    state = fields.Selection([('1', 'Player 1'), ('2', 'Player 2'), ('3', 'Launch')], default='1')
    
    def create_battle(self):
        self.ensure_one()
        self.env['runescape.battle'].create({
                            'player1':self.player1.id,
                            'player1_bet': self.player1_bet,
                            'player2': self.player2.id,
                            'player2_bet': self.player2_bet,
                            'date_start': self.date_start,
                            'date_end': self.date_end,
                            'state': self.state
                         })

    @api.onchange('player1')
    def _funcion(self):
        for s in self:
            player1_qty = self.env['res.partner'].search([('is_player',"=",True)])
            player1_qty = player1_qty.filtered(lambda r: r.id != s.player1.id)
            print(player1_qty)
            #return {'domain':{'player2'[('id','in',player1_qty.ids)]}}


    @api.onchange('player1_bet')
    def _get_player1_stats(self):
        for s in self:
            if s.player1.coins<s.player1_bet:
                s.player1_bet=s.player1.coins
                return {
                    'warning': {'title': "Warning", 'message': "No tienes suficientes coins!! Se ha puesto tu maximo de apuesta", 'type': 'notification'},
            }           
                

    @api.onchange('player2_bet')
    def _get_player2_stats(self):
        for s in self:
            if s.player2.coins<s.player2_bet:
                s.player2_bet=s.player2.coins
                return {
                    'warning': {'title': "Warning", 'message': "No tienes suficientes coins!! Se ha puesto tu maximo de apuesta", 'type': 'notification'},
                }

    def launch_battle(self):
        for s in self:
            player1_health = s.player1.hp
            player2_health = s.player2.hp
            while player1_health>0 and player2_health>0:
                damage_dealt_player1=(randrange(0,int(s.player1.damage*s.player1.strength/s.player1.defense),1))
                player2_health -=damage_dealt_player1
                damage_dealt_player1_str = "Damage by Player 1: "+str(damage_dealt_player1)+", Player 2 remaining hp : "+str(player2_health)

                damage_dealt_player2 = ( randrange(0, int(s.player2.strength*s.player2.damage/s.player2.defense), 1))
                player1_health -=damage_dealt_player2
                damage_dealt_player2_str ="Damage by Player 2: "+str(damage_dealt_player2)+", Player 1 remaining hp : "+str(player1_health)

                print(damage_dealt_player1_str)
                print(damage_dealt_player2_str)
            if player1_health>0:
                s.player1.coins+=s.player2_bet
                print("Player 1 wins, coins gain: "+str(s.player2_bet))
            else:
                s.player2.coins+=s.player1_bet
                print("Player 2 wins, coins gain: "+str(s.player1_bet))
            return{
            'name': 'Create Battle',
            'type': 'ir.actions.act_window',
            'res_model': 'runescape.battle_wizard',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id
        }
            

    def back(self):
        if self.state == '2':
            self.state = '1'
        if self.state == '3':
            self.state = '2'
        return{
            'name': 'Create Battle',
            'type': 'ir.actions.act_window',
            'res_model': 'runescape.battle_wizard',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id
        }

    def next(self):
        
        if self.state == '2':
                self.state = '3'
        if self.state == '1':
                self.state = '2'
        return{
            'name': 'Create Battle',
            'type': 'ir.actions.act_window',
            'res_model': 'runescape.battle_wizard',
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id
        }

