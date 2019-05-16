# -*- coding: utf-8 -*-
"""
Created on Tue May  7 14:39:22 2019

@author: Pedro
"""
import pygame as pg
import Cores as cores
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
        #self.player_img=pg.image.load(os.path.join(img_folder, 'imagem.png')).convert()
        self.image.set_colorkey(cores.WHITE)
        self.image=pg.transform.scale(self.image, (50,40))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x
        self.y = y
        self.energy = 100
        self.tired= 0
        self.hungry = 0

    def get_keys(self):
        self.vx,self.vy=0,0
        keys=pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx= -(cores.PLAYER_SPEED)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx= cores.PLAYER_SPEED
        elif keys[pg.K_UP] or keys[pg.K_w]:
            self.vy= -(cores.PLAYER_SPEED)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy= cores.PLAYER_SPEED
        #Para que serve?
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
            
    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def collide_with_walls(self,dx=0,dy=0):
        for wall in self.game.walls:
            if wall.x==self.x+dx and wall.y==self.y+dy:
                return True
            
    def update(self):
        self.rect.x = self.x * cores.TILESIZE
        self.rect.y = self.y * cores.TILESIZE
        self.get_keys()
        self.x += self.vx*self.game.dt
        self.y += self.vy*self.game.dt
        self.rect.topleft=(self.x,self.y)
        
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
        self.rect.x = x #* cores.TILESIZE
        self.rect.y = y #* cores.TILESIZE
    def recharge(self,player):
        player.energy = 100
        time.sleep (3)

class food (pg.sprite.Sprite):
    def __init__ (self,game,x,y,hungry):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.image = pg.Surface ((cores.TILESIZE, cores.TILESIZE))
        self.rect = self.image.get_rect()
        self.image.fill(cores.RED)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.hungry = hungry
        
    def done (self):
        self.kill()

class Text (pg.sprite.Sprite):
    def __init__ (self,game,x,y,text):
        self.font = pg.font.Font('freesansbold.ttf', 32) 
        self.text = self.font.render('Voce esta perdido numa ilha', True, cores.WHITE, cores.BLACK) 
        self.textRect = text.get_rect()   
        self.textRect.center = (x // cores.WIDTH, y // cores.HEIGHT)      
        
    #def update(self,image):
        #self.image.set_colorkey(cores.BLACK)

class mapa:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * cores.TILESIZE
        self.height = self.tileheight * cores.TILESIZE
        
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
    
def sumir_comida(food):
    food.image = pg.Surface ((0.5,0.5))
    food.image.fill(cores.WHITE)
    
def trocar_cenario(wallpaper):
    wallpaper.background = pg.image.load(path.join(img_dir, 'cenario.png')).convert()