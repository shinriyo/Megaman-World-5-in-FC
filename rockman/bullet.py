#!/usr/bin/env python
#coding: utf-8
import pygame

class Bullet(pygame.sprite.Sprite):
    speed = 9
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.top < 0:
            self.kill()

