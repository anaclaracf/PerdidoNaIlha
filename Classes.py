# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:39:22 2019

@author: Pedro
"""
import pygame as pg
import Cores as cores
import time

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((cores.TILESIZE, cores.TILESIZE))
        self.image.fill(cores.YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.energy = 100
        self.tired= 0 

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * cores.TILESIZE
        self.rect.y = self.y * cores.TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((cores.TILESIZE, cores.TILESIZE))
        self.image.fill(cores.GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * cores.TILESIZE
        self.rect.y = y * cores.TILESIZE
    
class Bed(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((cores.TILESIZE, cores.TILESIZE))
        self.image.fill(cores.WHITE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * cores.TILESIZE
        self.rect.y = y * cores.TILESIZE
    def recharge(self,player):
        player.energy = 100
        time.sleep (3)