# -*- coding: utf-8 -*-
"""
Created on Fri May  3 21:28:58 2019

@author: User
"""
import pygame as pg
import sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock =pg.time.Clock()
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
            self.dt=self.clock.tick(FPS)/1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()
    def update(self):
        self.all_sprites.update()
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        pg.display.flip()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
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