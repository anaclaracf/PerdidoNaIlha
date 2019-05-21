#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:16:22 2019

@author: beatrizcf
"""

import pygame as pg
import sys
from os import path
import settings
import sprites
import tilemap
import random
import time
img_dir = path.join(path.dirname(__file__), 'img')

font_name=pg.font.match_font('arial')

def draw_text(surf,text,size,x,y):
    font=pg.font.Font(font_name,size)
    text_surface=font.render(text,True,settings.WHITE)
    text_rect=text_surface.get_rect()
    text_rect.midtop=(x,y)
    surf.blit(text_surface, text_rect)
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pg.display.set_caption(settings.TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = tilemap.Map(path.join(game_folder, 'map2.txt'))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.dia=0
        self.tabuas=0
        self.cordas=0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bed = pg.sprite.Group()
        self.comida = pg.sprite.Group()
        self.madeira = sprites.wood(self,random.randrange(0,800),random.randrange(0,800))
        self.cordas_classe = sprites.rope (self,random.randrange(0,800),random.randrange(0,800))
        self.inimigo = pg.sprite.Group()
        self.comidas=[]
        for i in range(10):    
            self.comidas.append(sprites.food(self,random.randrange(0,500),random.randrange(0,500),4))
            self.all_sprites.add(self.comidas[i])
            self.comida.add(self.comidas[i])
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    sprites.Wall(self, col, row)
                if tile == 'P':
                    self.player = sprites.Player(self, col, row)
                    self.all_sprites.add(self.player)
                if tile == 'b':
                    self.bed = sprites.Bed(self,col,row)
                if tile == 'e':
                    self.inimigo = sprites.canibais(self,col,row)
                    
        self.camera = tilemap.Camera(self.map.width, self.map.height)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(settings.FPS) / 1000
            self.events()
            self.update()
            self.draw()
            self.win()
            #self.dia+=1

    def quit(self):
        pg.quit()
        sys.exit()

    def win (self):
       if self.tabuas == 5 and self.cordas==3:
               self.background = pg.image.load(path.join(img_dir, "youwin.png")).convert()
               self.background_rect = self.background.get_rect()
               self.background=pg.transform.scale(self.background, (200,150))
               time.sleep(2)
               self.quit()
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY, (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY, (0, y), (settings.WIDTH, y))

    def draw(self):
        self.screen.fill(settings.BGCOLOR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()
        draw_text(self.screen,str('Energia:{0}'.format(self.player.energy)),18, settings.WIDTH/2, 10)
        draw_text(self.screen,str('Fome:{0}'.format(self.player.hungry)),18,settings.WIDTH/2,30)
        draw_text(self.screen,str('Vida:{0}'.format(self.player.health)),18,settings.WIDTH/2,50)
        draw_text(self.screen,str('Madeiras:{0}'.format(self.tabuas)),18,settings.WIDTH-70,10)
        draw_text(self.screen,str('Cordas:{0}'.format(self.cordas)),18,settings.WIDTH-70,30)
        draw_text(self.screen,str('Ataque:{0}'.format(self.player.damage)),18,50,settings.HEIGHT-80)
        draw_text(self.screen,str('Objetivo: Conseguir 3 cordas e 5 madeiras'),18,150,settings.HEIGHT-60)
        if self.tabuas==5 and self.cordas==3:    
            draw_text(self.screen,str('Você Ganhou'),70,settings.WIDTH/2,settings.HEIGHT/2)
        
        if self.inimigo.health>0:
            if self.player.x - self.inimigo.x<=400 and self.player.x - self.inimigo.x>=-400:
                if self.player.y - self.inimigo.y <=400 and self.player.y - self.inimigo.y>=-400:
                    draw_text(self.screen,str('Vida do inimigo:{0}'.format(self.inimigo.health)),18,settings.WIDTH-70,settings.HEIGHT/2)
        pg.display.flip()
        #if self.dia==300:
            #self.screen.fill(settings.BLACK)
            #self.background = pg.image.load(path.join(img_dir, 'cenarioNoite.png')).convert()
            #self.background_rect = self.background.get_rect()
        #if self.dia==600:
            #self.screen.fill(settings.BLACK)
            #self.background = pg.image.load(path.join(img_dir, 'cenarioEPF.png')).convert()
            #self.background_rect = self.background.get_rect()
            #self.dia = 0 

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                #Movimentação                    
                if event.key == pg.K_LEFT:
                    self.player.tired+=1
                if event.key == pg.K_RIGHT:
                    self.player.tired+=1                   
                if event.key == pg.K_UP:
                    self.player.tired+=1
                if event.key == pg.K_DOWN:
                    self.player.tired+=1
                if self.player.tired%10==0 and self.player.tired!=0:
                    self.player.energy-=10
                    self.player.hungry+=10
                if event.key == pg.K_SPACE:
                    print(self.player.x - self.inimigo.x)
                    if self.player.x - self.bed.x<=50 and self.player.x - self.bed.x>=-50:
                        if self.player.y - self.bed.y <=50 and self.player.y - self.bed.y>=-50:
                            self.player.x=self.bed.x   ###
                            self.player.y=self.bed.y
                            self.bed.recharge(self.player)
                            self.player.tired=0
                    for i in self.comidas:
                        if self.player.x - i.x<=50 and self.player.x - i.x>=-50:
                            if self.player.y - i.y <=50 and self.player.y - i.y>=-50:
                                if self.player.hungry>=4:
                                    self.player.hungry-=i.hungry
                                    random_x = random.randrange(0,500)
                                    random_y = random.randrange(0,500)
                                    i.done()                                
                                    self.comidas.append(sprites.food(self,random_x,random_y,4)) 
                    if self.player.x - self.madeira.x<=50 and self.player.x - self.madeira.x>=-50:
                        if self.player.y - self.madeira.y <=50 and self.player.y - self.madeira.y>=-50:
                            self.tabuas+=1
                            self.madeira.gotten()
                            random_x = random.randrange(0,500)
                            random_y = random.randrange(0,500)
                            self.madeira = sprites.wood(self,random_x,random_y)
                    if self.player.x - self.cordas_classe.x<=50 and self.player.x - self.cordas_classe.x>=-50:
                        if self.player.y - self.cordas_classe.y <=50 and self.player.y - self.cordas_classe.y>=-50:
                            self.cordas+=1
                            self.cordas_classe.gotten()
                            random_x = random.randrange(0,500)
                            random_y = random.randrange(0,500)
                            self.cordas_classe = sprites.rope(self,random_x,random_y)
                    if self.player.x - self.inimigo.x<=50 and self.player.x - self.inimigo.x>=-50:
                        if self.player.y - self.inimigo.y <=50 and self.player.y - self.inimigo.y>=-50:
                            self.player.health-=self.inimigo.damage
                            self.inimigo.health-=self.player.damage
                            self.inimigo.die()
                            
                                
                                
                    
                print("Fome={0}".format(self.player.hungry))
                print("Energia={0}".format(self.player.energy))
            if self.player.energy <= 0:
                pg.quit()
                sys.exit()
            if self.player.hungry >= 100:
                pg.quit()
                sys.exit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()