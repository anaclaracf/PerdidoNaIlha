# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:28:58 2019

@author: User
"""
import pygame as pg
import sys
import Cores as cores
#from settings import *
#from sprites import *

with open('Cores.py','r') as arquivo:
    definicao=arquivo.read()

print(definicao)
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((cores.WIDTH,cores.HEIGHT))
        pg.display.set_caption(cores.TITLE)
        self.clock =pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.load_data()
        
    def load_data(self):
        pass
    def new (self):
        #Inicia todas as variáveis e todos os setups para um novo jogo
        self.all_sprites=pg.sprite.Group()
    def run(self):
        #Loop do jogo - Falso para finalizar o jogo
        self.playing=True
        while self.playing:
            self.dt=self.clock.tick(cores.FPS)/1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()
    def update(self):
        self.all_sprites.update()
    def draw_grid(self):
        for x in range (0,cores.WIDTH,cores.TILESIZE):
            pg.draw.line(self.screen,cores.LIGHTGREY, (x,0),(x, cores.HEIGHT))
        for y in range (0,cores.HEIGHT,cores.TILESIZE):
            pg.draw.line(self.screen,cores.LIGHTGREY, (0,y),(cores.WIDTH, y))
    def draw(self):
        self.screen.fill(cores.BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_LEFT:
                    self.player.move(dy=1)
    def show_start_screen (self):
        pass
    
    def show_go_screen(self):
        pass

g=Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()