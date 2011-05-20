#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
from util import *
import os
import sys
from player import Player
from block import Block

class Map:
    """マップ（プレイヤーや内部のスプライトを含む）"""
    GS = 16  # gridsize (original:32)
    
    def __init__(self, filename):
        # スプライトグループの登録
        self.all = pygame.sprite.RenderUpdates()
        self.blocks = pygame.sprite.Group()
        Player.containers = self.all
        Block.containers = self.all, self.blocks
        
        # create player (first pos:x, y, block)
        # first position
        self.player = Player((100,110), self.blocks)
        
        # マップをロードしてマップ内スプライトの作成
        self.load(filename)
        
        # create map surface
        self.surface = pygame.Surface((self.col*self.GS, self.row*self.GS)).convert()
        
    def draw(self):
        """マップサーフェイスにマップ内スプライトを描画"""
        self.surface.fill((0,0,0))
        self.all.draw(self.surface)
    
    def update(self):
        """マップ内スプライトを更新"""
        self.all.update()
    
    def calc_offset(self):
        """オフセットを計算"""
        offsetx = self.player.rect.topleft[0] - SCR_RECT.width/2
        offsety = self.player.rect.topleft[1] - SCR_RECT.height/2
        return offsetx, offsety

    def load(self, filename):
        """マップをロードしてスプライトを作成"""
        map = []
        fp = open(filename, "r")
        for line in fp:
            line = line.rstrip()  # 改行除去
            map.append(list(line))

        self.row = len(map)
        self.col = len(map[0])
        self.width = self.col * self.GS
        self.height = self.row * self.GS
        fp.close()
        
        # マップからスプライトを作成
        for i in range(self.row):
            for j in range(self.col):
                asciicode = ord(map[i][j]) # ブロックNO
                # ord() method convert to number from character
                #if not asciicode == 32('半角スペース'):
                if not asciicode in [32, 33, 71, 72, 73, 77, 78, 79, 80, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113]:
                    Block((j*self.GS, i*self.GS), asciicode-33).image

