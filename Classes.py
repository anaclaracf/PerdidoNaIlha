# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:39:22 2019

@author: Pedro
"""
import pygame as pg
import Cores as cores

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game= game
        self.image=pg.Surface(cores.TILESIZE,cores.TILESIZE)
        self.image.fill(cores.BLUE)
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
    
    def move(self,dx=0,dy=0):
        self.x+=dx
        self.y+=dy
    
    def update(self):
        self.rect.x=self.x * cores.TILESIZE
        self.rect.y=self.y *cores.TILESIZE
        
class Parede (pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all