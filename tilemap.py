#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 17 14:20:45 2019

@author: beatrizcf
"""
import pytmx
import pygame as pg
import settings

def collide_hit_rect (one,two):
    return one.hit_rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * settings.TILESIZE
        self.height = self.tileheight * settings.TILESIZE
        
class TiledMap:
    def __init__ (self,filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width*tm.tilewidth
        self.height = tm.height*tm.tileheight
        self.tmxdata = tm
        
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance (layer, pytmx.TiledTileLayer):
                for x,y,gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))
    def Makemap(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

    
class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
       return rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(settings.WIDTH / 2)
        y = -target.rect.centery + int(settings.HEIGHT / 2)
        x = min(0, x)  
        y = min(0, y)  
        x = max(-(self.width - settings.WIDTH), x)  
        y = max(-(self.height - settings.HEIGHT), y)  
        self.camera = pg.Rect(x, y, self.width, self.height)
