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
        #self.player_img=pg.image.load(os.path.join(img_folder, 'imagem.png')).convert()
        #self.image.set_colorkey(cores.BLACK)
        #self.image=pg.transform.scale(self.player_img, (100,80))
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0,0
        self.x = x
        self.y = y
        self.energy = 100
        self.tired= 0 

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