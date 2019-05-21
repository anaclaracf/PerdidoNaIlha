#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:20:13 2019

@author: beatrizcf
"""

import pygame as pg
import settings
import time
import random
from os import path
import os

vec = pg.math.Vector2

from tilemap import collide_hit_rect

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        #self.image.set_colorkey(settings.WHITE)
        #self.image=pg.transform.scale(self.image, (50,40))
        self.rect = self.image.get_rect()
        self.hit_rect = settings.PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0,0) #velocity vector
        self.pos = vec(x,y) * settings.TILESIZE #position vector
        self.rot = 0 
        self.hungry = settings.PLAYER_HUNGRY
        self.health = settings.PLAYER_HEALTH
        self.energy = settings.PLAYER_ENERGY
        self.tired=0
        self.health = 100
        self.damage = 10
        self.tabuas = 0
        self.cordas = 0
        
    def get_keys(self):
        self.vel = vec(0,0)
        self.rot_speed = 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = settings.PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -settings.PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(settings.PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-settings.PLAYER_SPEED/2 , 0).rotate(-self.rot)

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width/2 
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right +  self.hit_rect.width/2 
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height/2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rot = (self.rot + self.rot_speed*self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y') 
        self.rect.center = self.hit_rect.center
        #self.hungry += 1
        #self.energy -= 0.5
        if self.energy<0 or self.hungry>1000:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.image.fill(settings.GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
    
class Bed(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((settings.TILESIZE,settings.TILESIZE))
        self.image.fill(settings.WHITE)
        self.rect = self.image.get_rect()
        self.x = x * settings.TILESIZE
        self.y = y * settings.TILESIZE
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
        
    def recharge(self,player):
        player.energy = 100
        time.sleep (3)

class food (pg.sprite.Sprite):
    def __init__ (self,game,x,y,hungry):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface ((settings.TILESIZE,settings.TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(settings.RED)
        self.x = x #* settings.TILESIZE
        self.y = y #* settings.TILESIZE
        self.rect.x = x #* settings.TILESIZE
        self.rect.y = y #* settings.TILESIZE
        self.hungry = settings.FOOD_NUTRI
        
    def done (self):
        self.kill()

class wood (pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface ((settings.TILESIZE,settings.TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(settings.GREEN)
        self.x = x #* settings.TILESIZE
        self.y = y #* settings.TILESIZE
        self.rect.x = x #* settings.TILESIZE
        self.rect.y = y #* settings.TILESIZE
        
    def gotten (self):
        self.kill()
        
class rope (pg.sprite.Sprite):
    def __init__ (self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface ((settings.TILESIZE,settings.TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(settings.LIGHTGREY)
        self.x = x #* settings.TILESIZE
        self.y = y #* settings.TILESIZE
        self.rect.x = x #* settings.TILESIZE
        self.rect.y = y #* settings.TILESIZE
        
    def gotten (self):
        self.kill()
    
class canibais(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill (settings.YELLOW)
        self.x = x * settings.TILESIZE
        self.y= y * settings.TILESIZE
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE
        self.damage = 5
        self.health = 30
        
    def die(self):
        if self.health <=0:
            self.kill()
        
inventario = {
        'roupas': {
                'calça': ' algodao',
                'camisa': ' éter',
                'sapato':'couro'
                },
        'comida': {
                },
        'recursos':{
                },
        'armas' : {
                }        
        }
    