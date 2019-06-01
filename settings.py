#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:19:13 2019
@author: beatrizcf
"""
import pygame as pg

#Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
BRIGHT_GREEN = (0, 200, 0)
RED = (255, 0, 0)
BRIGHT_RED = (200, 0, 0)
YELLOW = (255, 255, 0)

# Config do game
WIDTH = 1024   
HEIGHT = 768  
FPS = 60
TITLE = "Escape the Island"
BGCOLOR = DARKGREY

TILESIZE = 8
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

FONT_NAME = pg.font.match_font('arial')

# Player
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 175
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
PLAYER_ENERGY = 50
PLAYER_HUNGRY = 100
PLAYER_HEALTH = 100
PLAYER_IMG = 'manBlue_gun.png'

#Food
FOOD_NUTRI = 10
COMIDA_IMG = 'pizza.png'

#Monstro
MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0,0,30,30)

#Madeira
MADEIRA_IMG='madeira.png'

#Corda
CORDA_IMG='corda.png'

#Cama
CAMA_IMG='bed.png'

#Quadro
QUADRO = 'quadro.png'

#TOCHA
TOCHA = 'tocha.png'