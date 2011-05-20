#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
from util import *
import os
import sys
from map import Map
from block import Block

SCR_RECT = Rect(0, 0, 640, 480)
# MODE


class PyAction:
    def __init__(self, type=1):
        pygame.init()
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("ROCKMAN WORLD 5")
        
        # load images
        Block.images = split_image(load_image("plute_map.png"), 16, 16, 16)
        Block.image = Block.images[0] #初期化

        # music
#        pygame.mixer.music.load("data/mars.nsf")
#        pygame.mixer.music.play(-1) 
        
        # loading map
        self.map = Map("data/plute.map")
        
        # main loop
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            pygame.display.update()
            self.key_handler()

    def update(self):
        self.map.update()
    
    def draw(self, screen):
        self.map.draw()
        
        # draw part of map by offset
        offsetx, offsety = self.map.calc_offset()
        
        # 端ではスクロールしない
        if offsetx < 0:
            offsetx = 0
        elif offsetx > self.map.width - SCR_RECT.width:
            offsetx = self.map.width - SCR_RECT.width
        
        if offsety < 0:
            offsety = 0
        elif offsety > self.map.height - SCR_RECT.height:
            offsety = self.map.height - SCR_RECT.height
        
        # マップの一部を画面に描画
        screen.blit(self.map.surface, (0,0), (offsetx, offsety, SCR_RECT.width, SCR_RECT.height))
    
    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

def load_image(filename, colorkey=None):
#-----
    try:
        import SDL_image
        print "Loaded SDL_image"
    except:
        print "Failed to import SDL_image"

    try:
        import libpng
        print "Loaded libpng"
    except:
        print "Failed to import libpng"
#-----

    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

if __name__ == "__main__":
    PyAction()
