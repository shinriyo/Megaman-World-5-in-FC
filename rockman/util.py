#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from util import *
import sys
import os

SCR_RECT = Rect(0, 0, 640, 480)
GS = 32

DOWN,LEFT,RIGHT,UP = 0,1,2,3

def load_image(filename):

    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    image = image.convert_alpha()

    return image

def split_image(image, w=18, h=8, rect_size=GS):
    imageList = [] # リストの初期化
    for i in range(0, h*rect_size, rect_size):
        for j in range(0, w*rect_size, rect_size):
            surface = pygame.Surface((rect_size, rect_size))
            surface.blit(image, (0,0), (j, i, rect_size, rect_size))
            surface.convert_alpha() # 透明色にする
            imageList.append(surface)
    return imageList
