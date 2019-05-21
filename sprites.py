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

img_dir = path.join(path.dirname(__file__), 'img')

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load(path.join(img_dir, "homem.png")).convert()
        self.image.set_colorkey(settings.WHITE)
        self.image=pg.transform.scale(self.image, (50,40))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * settings.TILESIZE
        self.y = y * settings.TILESIZE
        self.energy = 100
        self.tired= 0
        self.hungry = 0
        self.health = 100
        self.damage = 10
        
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -settings.PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = settings.PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -settings.PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = settings.PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

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
        self.hungry = hungry
        
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
    