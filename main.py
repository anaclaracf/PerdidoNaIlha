#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:16:22 2019
@author: beatrizcf
"""
#

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
font_name2=pg.font.match_font('Felix Titling')

gameDisplay = pg.display.set_mode((settings.WIDTH,settings.HEIGHT))
pg.display.set_caption("ESCAPE THE ISLAND")
clock = pg.time.Clock()
 
def text_objects(text, font):
    textSurface = font.render(text, True, settings.WHITE)
    return textSurface, textSurface.get_rect()

def message_display(text,pg):
    largeText = pg.font.Font(font_name,90)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((settings.WIDTH/2),(settings.HEIGHT/2))
    gameDisplay.blit(TextSurf, TextRect)
    pg.display.update()
    time.sleep(2)
    game_loop()

                            
class game_intro:
    def __init__(self,game):
        pg.init()
        intro = True
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type ==pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        intro=False
            background= pg.image.load(path.join(img_dir, "fundo2.png")).convert()
            gameDisplay.blit(background, background.get_rect())
            
            pg.display.update()
        
        background = pg.image.load(path.join(img_dir,"apresentaçao.png")).convert()
        gameDisplay.blit(background, background.get_rect())
        pg.display.update()
        time.sleep(3)
        background = pg.image.load(path.join(img_dir,"como jogar.png")).convert()
        gameDisplay.blit(background, background.get_rect())
        pg.display.update()
        time.sleep(3) 
		  
        g = Game()
        g.show_start_screen()
        while True:
            g.new()
            g.run()   
            g.show_go_screen()

def draw_text(surf,text,size,x,y):
    font=pg.font.Font(font_name,size)
    text_surface=font.render(text,True,settings.BLACK)
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
        snd_folder = path.join(game_folder,'snd')
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map')
        self.snd_background=pg.mixer.Sound(path.join(snd_folder,'gaivota.wav'))
        self.map = tilemap.TiledMap(path.join(map_folder, 'labirinto.tmx'))
        self.map_img = self.map.Makemap() 
        self.map_rect = self.map_img.get_rect()
        self.inimigo_img=pg.image.load(path.join(img_folder, settings.PLAYER_IMG)).convert_alpha()
        self.player_img=pg.image.load(path.join(img_folder, settings.PLAYER_IMG)).convert_alpha()
        self.madeira_img = pg.image.load(path.join(img_folder,settings.MADEIRA_IMG)).convert_alpha()
        self.corda_img = pg.image.load(path.join(img_folder,settings.CORDA_IMG)).convert_alpha()
        self.comida_img = pg.image.load(path.join(img_folder,settings.COMIDA_IMG)).convert_alpha()
        self.cama_img = pg.image.load(path.join(img_folder,settings.CAMA_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.snd_background.play()
        self.dia=0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.bed = pg.sprite.Group()
        self.beds=[]
        self.comida = pg.sprite.Group()
        #self.madeira = sprites.wood(self,random.randrange(0,800),random.randrange(0,800))
        #self.cordas_classe = sprites.rope (self,random.randrange(0,800),random.randrange(0,800))
        self.cordas=[]
        self.corda=pg.sprite.Group() 
        self.madeiras=[]
        self.madeira=pg.sprite.Group()
        self.inimigo = pg.sprite.Group()
        self.inimigos=[]
        self.comidas=[]
        for i in range(10):    
            self.comidas.append(sprites.food(self,random.randrange(0,500),random.randrange(0,500),4))
            self.all_sprites.add(self.comidas[i])
            self.comida.add(self.comidas[i])
        #for row, tiles in enumerate(self.map.data):
            #for col, tile in enumerate(tiles):
                #if tile == '1':
                    #sprites.Wall(self, col, row)
                #if tile == 'P':
                    #self.player = sprites.Player(self, col, row)
                    #self.all_sprites.add(self.player)
                #if tile == 'b':
                    #self.bed = sprites.Bed(self,col,row)
                #if tile == 'e':
                    #self.inimigo = sprites.canibais(self,col,row)
                    #self.inimigos.append(self.inimigo)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'player':
                self.player = sprites.Player(self,tile_object.x, tile_object.y)
            if tile_object.name == 'madeira':
                self.madeira = sprites.wood(self,tile_object.x, tile_object.y)
                self.madeiras.append(self.madeira)
                self.all_sprites.add(self.madeira)
            if tile_object.name == 'comida':
                self.comida= sprites.food(self,tile_object.x,tile_object.y,4)
                self.comidas.append(self.comida)
                self.all_sprites.add(self.comida)
            if tile_object.name == 'barreira':
                self.obstacle = sprites.Obstacle(self,tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            #if tile_object.name == 'Indio':
                #self.inimigo = sprites.canibais(self,tile_object.x, tile_object.y)
                #self.inimigos.append(self.inimigo)
                #self.all_sprites.add(self.inimigo)
            if tile_object.name == 'corda':
                self.corda = sprites.rope(self,tile_object.x, tile_object.y)
                self.cordas.append(self.corda)
                self.all_sprites.add(self.corda)
            if tile_object.name == 'bed':
                self.bed = sprites.Bed(self,tile_object.x, tile_object.y)
                self.beds.append(self.bed)
                self.all_sprites.add(self.bed)
            if tile_object.name == 'vitoria':
                self.vitoriax= tile_object.x
                self.vitoriay= tile_object.y
        #self.player = sprites.Player(self,5,5)
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
            self.check_damage()
            self.dia+=1
            self.morte()
    def quit(self):
        pg.quit()
        sys.exit()

    def win (self):
       if self.player.tabuas == 5 and self.player.cordas == 3:
           if self.player.pos.x - self.vitoriax<=50 and self.player.pos.x - self.vitoriax>=-50:
                    if self.player.pos.y - self.vitoriay <=50 and self.player.pos.y - self.vitoriay>=-50:
                        background = pg.image.load(path.join(img_dir, "final.png")).convert()
                        gameDisplay.blit(background, background.get_rect())               
                        pg.display.update()
                        time.sleep(2)
                        pg.init()
                        intro = True
                        while intro:
                            clock.tick(15)
                            for event in pg.event.get():
                                 if event.type == pg.QUIT:
                                     pg.quit()
                                     sys.exit()
                                 if event.type ==pg.KEYDOWN:
                                     if event.key==pg.K_SPACE:
                                         intro=False
                            background= pg.image.load(path.join(img_dir, "fundo2.png")).convert()
                            gameDisplay.blit(background, background.get_rect())
            
                            pg.display.update()
                        
                        g = Game()
                        g.show_start_screen()
                        while True:
                            g.new()
                            g.run()
              
    def check_damage(self):
        if self.dia%60==0:
            for sprite in self.inimigos:
                if sprite.health>0:
                    if self.player.pos.x - sprite.pos.x<=50 and self.player.pos.x - sprite.pos.x>=-50:
                        if self.player.pos.y - sprite.pos.y <=50 and self.player.pos.y - sprite.pos.y>=-50:
                            self.player.health-=sprite.damage
    
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
            
    def morte(self):        
        if self.player.health<=0 :
            background=pg.image.load(path.join(img_dir, "game over.png")).convert()
            gameDisplay.blit(background, background.get_rect())
            pg.display.update()
            time.sleep(2)
            pg.init()
            intro = True
            while intro:
                clock.tick(15)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                         pg.quit()
                         sys.exit()
                    if event.type ==pg.KEYDOWN:
                        if event.key==pg.K_SPACE:
                            intro=False
                background= pg.image.load(path.join(img_dir, "fundo2.png")).convert()
                gameDisplay.blit(background, background.get_rect())

                pg.display.update()
            
            g = Game()
            g.show_start_screen()
            while True:
                g.new()
                g.run()   
                g.show_go_screen()   
        if self.player.energy <= 0 or self.player.hungry >= 100:
            if self.dia%60==0:
                self.player.health-=5

    def draw_grid(self):
        for x in range(0, settings.WIDTH, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY, (x, 0), (x, settings.HEIGHT))
        for y in range(0, settings.HEIGHT, settings.TILESIZE):
            pg.draw.line(self.screen, settings.LIGHTGREY, (0, y), (settings.WIDTH, y))
    
    def draw_text(self,text,size,x,y):
        font=pg.font.Font(font_name,size)
        text_surface=font.render(text,True,settings.WHITE)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        #self.screen.fill(settings.BGCOLOR)
        #self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite,sprites.Player):
                sprite.draw_life()
            if isinstance(sprite,sprites.canibais):
                sprite.draw_life()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_text(str('Energia:{0}'.format(self.player.energy)),18, settings.WIDTH/2, 10)
        self.draw_text(str('Fome:{0}'.format(self.player.hungry)),18,settings.WIDTH/2,30)
        self.draw_text(str('Vida:{0}'.format(self.player.health)),18,settings.WIDTH/2,50)
        self.draw_text(str('Madeiras:{0}'.format(self.player.tabuas)),18,settings.WIDTH-70,10)
        self.draw_text(str('Cordas:{0}'.format(self.player.cordas)),18,settings.WIDTH-70,30)
        self.draw_text(str('Ataque:{0}'.format(self.player.damage)),18,50,settings.HEIGHT-80)
        if self.player.tabuas<5 or self.player.cordas<3:
            self.draw_text(str('Objetivo: Conseguir 3 cordas e 5 madeiras'),18,200,settings.HEIGHT-150)
        else:
            self.draw_text(str('Objetivo: Escape pelo barco'),18,200,settings.HEIGHT-150)
        for sprite in self.inimigos:
            if sprite.health>0:
                if self.player.pos.x - sprite.pos.x<=400 and self.player.pos.x - sprite.pos.x>=-400:
                    if self.player.pos.y - sprite.pos.y <=400 and self.player.pos.y - sprite.pos.y>=-400:
                        self.draw_text(str('Vida do inimigo:{0}'.format(sprite.health)),18,settings.WIDTH-70,settings.HEIGHT/2)
                        sprite.persecution()
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
                    self.player.tired+=10
                if event.key == pg.K_RIGHT:
                    self.player.tired+=10                   
                if event.key == pg.K_UP:
                    self.player.tired+=10
                if event.key == pg.K_DOWN:
                    self.player.tired+=10
                if self.player.tired>10:
                    self.player.energy-=1
                    self.player.hungry+=1
                    self.player.tired=0
                if event.key == pg.K_SPACE:
                    #print(self.player.x - self.inimigo.x)
                    for sprite in self.beds:
                        if self.player.pos.x - sprite.x<=100 and self.player.pos.x - sprite.x>=-100:
                            if self.player.pos.y - sprite.y <=100 and self.player.pos.y - sprite.y>=-100:
                                self.player.pos.x=sprite.x   ###
                                self.player.pos.y=sprite.y
                                sprite.recharge(self.player)
                                self.player.tired=0
                                self.player.health=100
                    for i in self.comidas:
                        if self.player.pos.x - i.x<=50 and self.player.pos.x - i.x>=-50:
                            if self.player.pos.y - i.y <=50 and self.player.pos.y - i.y>=-50:
                                if self.player.hungry>=4:
                                    self.player.hungry-=i.hungry
                                    random_x = random.randrange(0,500)
                                    random_y = random.randrange(0,500)
                                    i.done()                                
                                    self.comidas.append(sprites.food(self,random_x,random_y,4)) 
                                    if self.player.hungry<0:
                                        self.player.hungry=0
#                    if self.player.pos.x - self.madeira.x<=50 and self.player.pos.x - self.madeira.x>=-50:
#                        if self.player.pos.y - self.madeira.y <=50 and self.player.pos.y - self.madeira.y>=-50:
#                            self.player.tabuas+=1
#                            self.madeira.gotten()
#                            random_x = random.randrange(0,500)
#                            random_y = random.randrange(0,500)
#                            if self.player.tabuas<5:
#                                self.madeira = sprites.wood(self,random_x,random_y)
                    for sprite in self.madeiras:
                        if self.player.pos.x - sprite.x<=50 and self.player.pos.x - sprite.x>=-50:
                            if self.player.pos.y - sprite.y <=50 and self.player.pos.y - sprite.y>=-50:
                                self.player.tabuas+=sprite.quantidade
                                sprite.gotten()
                                random_x = random.randrange(0,500)
                                random_y = random.randrange(0,500)
                            #if self.player.tabuas<5:
                                #self.madeira = sprites.wood(self,random_x,random_y)
                    for sprite in self.cordas:
                        if self.player.pos.x - sprite.x<=50 and self.player.pos.x - sprite.x>=-50:
                            if self.player.pos.y - sprite.y <=50 and self.player.pos.y - sprite.y>=-50:
                                self.player.cordas+=sprite.quantidade
                                sprite.gotten()
                                random_x = random.randrange(0,500)
                                random_y = random.randrange(0,500)
                            #if self.player.cordas<3:
                                #self.cordas_classe = sprites.rope(self,random_x,random_y)
                    for sprite in self.inimigos:
                        if self.player.pos.x - sprite.pos.x<=50 and self.player.pos.x - sprite.pos.x>=-50:
                            if self.player.pos.y - sprite.pos.y <=50 and self.player.pos.y - sprite.pos.y>=-50:
                                sprite.health-=self.player.damage
                                sprite.die()
                            
                                
                                
                    
                print("Fome={0}".format(self.player.hungry))
                print("Energia={0}".format(self.player.energy))

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


game_intro(pg)
# create the game object
