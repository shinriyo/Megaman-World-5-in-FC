#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import sys
from util import *

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, tip_no):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.image = self.images[tip_no]

