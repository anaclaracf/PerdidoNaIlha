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
font_name2=pg.font.match_font('FelixTitling')

gameDisplay = pg.display.set_mode((settings.WIDTH,settings.HEIGHT))
pg.display.set_caption("PERDIDO NA ILHA")
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

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse [1] > y:
        pg.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            if action == "play":
                g = Game()
                g.show_start_screen()
                while True:
                    g.new()
                    g.run()
                    g.show_go_screen()
            elif action == "quit":
                pg.quit()
                sys.exit()
                
    else:
        pg.draw.rect(gameDisplay, ic, (x, y, w, h))
    smallText = pg.font.Font(font_name2, 30)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
                
                
class game_intro:
    def __init__(self,game):
        pg.init()
        intro = True
        while intro:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            background= pg.image.load(path.join(img_dir, "Fundo3.png")).convert()
            gameDisplay.blit(background, background.get_rect())
            largeText = pg.font.Font(font_name2,115)
            TextSurf, TextRect = text_objects("ESCAPE THE ISLAND", largeText)
            TextRect.center = ((settings.WIDTH/2),(settings.HEIGHT/2))
            gameDisplay.blit(TextSurf, TextRect)
            
            button("GO!",350, 500, 100, 50,settings.BLACK,settings.LIGHTGREY,"play")
            button("QUIT",550, 500, 100, 50,settings.BLACK,settings.LIGHTGREY,"quit")
        
            
            pg.display.update()
            clock.tick(15)

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
        img_folder = path.join(game_folder, 'img')
        self.map = tilemap.Map(path.join(game_folder, 'map2.txt'))
        self.player_img=pg.image.load(path.join(img_folder, settings.PLAYER_IMG)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.dia=0
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
       if self.player.tabuas == 5 and self.player.cordas==3:
               #background = pg.image.load(path.join(img_dir, "youwin.png")).convert()
               #gameDisplay.blit(background, background.get_rect())
               self.background = pg.image.load(path.join(img_dir, "youwin.png")).convert()
               self.background_rect = self.background.get_rect()
               self.background=pg.transform.scale(self.background, (200,150))
               #pg.display.update()
               time.sleep(4)
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
    def draw_text(self,text,size,x,y):
        font=pg.font.Font(font_name,size)
        text_surface=font.render(text,True,settings.WHITE)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(settings.BGCOLOR)
        self.draw_grid()
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
        self.draw_text(str('Objetivo: Conseguir 3 cordas e 5 madeiras'),18,150,settings.HEIGHT-60)
        if self.player.tabuas==5 and self.player.cordas==3:    
            self.draw_text(str('Você Ganhou'),70,settings.WIDTH/2,settings.HEIGHT/2)
        
        if self.inimigo.health>0:
            if self.player.pos.x - self.inimigo.pos.x<=400 and self.player.pos.x - self.inimigo.pos.x>=-400:
                if self.player.pos.y - self.inimigo.pos.y <=400 and self.player.pos.y - self.inimigo.pos.y>=-400:
                    self.draw_text(str('Vida do inimigo:{0}'.format(self.inimigo.health)),18,settings.WIDTH-70,settings.HEIGHT/2)
                    self.inimigo.persecution()
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
                    self.player.energy-=1
                    self.player.hungry+=1
                if event.key == pg.K_SPACE:
                    #print(self.player.x - self.inimigo.x)
                    if self.player.pos.x - self.bed.x<=50 and self.player.pos.x - self.bed.x>=-50:
                        if self.player.pos.y - self.bed.y <=50 and self.player.pos.y - self.bed.y>=-50:
                            self.player.pos.x=self.bed.x   ###
                            self.player.pos.y=self.bed.y
                            self.bed.recharge(self.player)
                            self.player.tired=0
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
                    if self.player.pos.x - self.madeira.x<=50 and self.player.pos.x - self.madeira.x>=-50:
                        if self.player.pos.y - self.madeira.y <=50 and self.player.pos.y - self.madeira.y>=-50:
                            self.player.tabuas+=1
                            self.madeira.gotten()
                            random_x = random.randrange(0,500)
                            random_y = random.randrange(0,500)
                            if self.player.tabuas<5:
                                self.madeira = sprites.wood(self,random_x,random_y)
                    if self.player.pos.x - self.cordas_classe.x<=50 and self.player.pos.x - self.cordas_classe.x>=-50:
                        if self.player.pos.y - self.cordas_classe.y <=50 and self.player.pos.y - self.cordas_classe.y>=-50:
                            self.player.cordas+=1
                            self.cordas_classe.gotten()
                            random_x = random.randrange(0,500)
                            random_y = random.randrange(0,500)
                            if self.player.cordas<3:
                                self.cordas_classe = sprites.rope(self,random_x,random_y)
                    if self.player.pos.x - self.inimigo.pos.x<=50 and self.player.pos.x - self.inimigo.pos.x>=-50:
                        if self.player.pos.y - self.inimigo.pos.y <=50 and self.player.pos.y - self.inimigo.pos.y>=-50:
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


game_intro(pg)
# create the game object
