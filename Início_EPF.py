# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:28:58 2019

@author: User
"""
import pygame as pg
import sys
import Cores as cores
import Classes as classes
import os
from os import path
import random

img_dir = path.join(path.dirname(__file__), 'img')
dia=0

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((cores.WIDTH, cores.HEIGHT))
        self.background = pg.image.load(path.join(img_dir, 'cenarioEPF.png')).convert()
        self.background_rect = self.background.get_rect()
        pg.display.set_caption(cores.TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        

    def load_data(self):
        game_folder=path.dirname(__file__)
        self.map_data=[]
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # Inicializa as variáveis
        self.dia=0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = classes.Player(self, 10, 10)
        self.bed = classes.Bed(self,300,300)
        self.comida = classes.food(self,random.randrange(0,500),random.randrange(0,500),4)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile=='1':
                    classes.Wall(self,col,row)
                #if tile=='b':
                    #self.bed=classes.Bed(self,col,row)

    def run(self):
        # Game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(cores.FPS) / 1000
            self.events()
            self.update()
            self.draw()
            self.dia+=1
                
            
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # Atualização do jogo
        self.all_sprites.update()

    def draw(self):
        ##Inicia parte gráficas
        self.screen.fill(cores.BGCOLOR)
        self.screen.blit(self.background, self.background_rect)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
        if self.dia==300:
            self.screen.fill(cores.BLACK)
            self.background = pg.image.load(path.join(img_dir, 'cenarioNoite.png')).convert()
            self.background_rect = self.background.get_rect()
        if self.dia==600:
            self.screen.fill(cores.BLACK)
            self.background = pg.image.load(path.join(img_dir, 'cenarioEPF.png')).convert()
            self.background_rect = self.background.get_rect()
            self.dia = 0 

    def events(self):
        # Eventos
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
            
                #Movimentação
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                    self.player.tired+=1
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                    self.player.tired+=1
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                    self.player.tired+=1
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)
                    self.player.tired+=1    
                if self.player.tired%10==0:
                    self.player.energy-=10
                    self.player.hungry+=10
                if event.key == pg.K_SPACE:
                    if self.player.x - self.bed.x<=20 and self.player.x - self.bed.x>=-20:
                        if self.player.y - self.bed.y <=20 and self.player.y - self.bed.y>=-20:
                            self.player.x=self.bed.x   ###
                            self.player.y=self.bed.y
                            self.bed.recharge(self.player)
                            self.player.tired=0
                    if self.player.x - self.comida.x<=20 and self.player.x - self.comida.x>=-20:
                        if self.player.y - self.comida.y <=20 and self.player.y - self.comida.y>=-20:
                            if self.player.hungry>=4:
                                self.player.hungry-=self.comida.hungry
                                random_x = random.randrange(0,500)
                                random_y = random.randrange(0,500)
                                self.comida.done()
                                #classes.sumir_comida(self.comida)                                
                                self.comida = classes.food(self,random_x,random_y,4)
                                
                                
                    
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

# Cria o objeto de jogo
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()