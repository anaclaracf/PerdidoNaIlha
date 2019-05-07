# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:39:22 2019

@author: Pedro
"""
import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game= game
        self.image=pg.Surface(TILESIZE,TILESIZE)
        self.image.fill(BLUE)
        self.rect=self.image.get_rect()
        self.x=x
        self.y=y
    
    def update(self):
        self.rect.x=self.x * TILESIZE
        self.rect.y=self.y *TILESIZE
        
