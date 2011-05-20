#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
from bullet import Bullet
from util import *
import os
import sys

class Player(pygame.sprite.Sprite):
    """ ロックマン """
    MOVE_SPEED = 2.5    # 移動速度
    JUMP_SPEED = 10.0    # ジャンプの初速度
    GRAVITY = 0.5       # 重力加速度
    MAX_JUMP_COUNT = 1  # ジャンプ段数の回数
    DIRECTION_RIGHT = 1
    DIRECTION_LEFT = 2
    STATUS_START = 5
    STATUS_NORMAL = 1
    STATUS_DAMAGE = 2
    STATUS_CHARGE = 3
    STATUS_MAXCHARGE = 4

    animcycle = 6  # アニメーション速度 24
    frame = 0
    direction = DIRECTION_RIGHT
    status = STATUS_START
    reload_time = 15

    def __init__(self, pos, blocks, name="rockman"):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images = split_image(load_image("%s.png" % name)) #sss

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]  # 座標設定
        self.blocks = blocks  # 衝突判定用
        
        # ジャンプ回数
        self.jump_count = 0

        self.charge_time = 0
        
        # 浮動小数点の位置と速度
        self.fpx = float(self.rect.x)
        self.fpy = float(self.rect.y)
        self.fpvx = 0.0
        self.fpvy = 0.0
        
        # on floor or not
        self.on_floor = False

        all = pygame.sprite.RenderUpdates()
        Bullet.containers = all

        Bullet.image = self.images[2]
        self.reload_timer = 0
 
    def update(self):
        self.frame += 1
        """スプライトの更新"""
        # キー入力取得
        pressed_keys = pygame.key.get_pressed()
#        released_keys = pygame.key.get_released()

        # jumping
        if self.on_floor == False:
            # geme starting player
            if self.status == self.STATUS_START:
               self.image = self.images[0] # long body
            elif self.direction == self.DIRECTION_RIGHT:
               self.image = self.images[18 + 6] #ジャンプ画像
            elif self.direction == self.DIRECTION_LEFT:
                self.image = pygame.transform.flip(self.images[18 + 6], 1, 0)
        # KEY mapping
        if pressed_keys[K_RIGHT]:
            self.direction = self.DIRECTION_RIGHT
            if self.on_floor:
                self.image = self.images[18 + 3 + self.frame / self.animcycle % 3]
            self.fpvx = self.MOVE_SPEED
        elif pressed_keys[K_LEFT]:
            self.direction = self.DIRECTION_LEFT
            if self.on_floor:
                self.image = pygame.transform.flip(self.images[18 + 3 + self.frame / self.animcycle % 3], 1, 0)
            self.fpvx = -self.MOVE_SPEED
        # standing
        elif self.on_floor:
            self.fpvx = 0.0
            if self.direction == self.DIRECTION_RIGHT:
                self.image = self.images[18 + (self.charge_time % 3) * 18 + 0 + self.frame / self.animcycle % 2]
            elif self.direction == self.DIRECTION_LEFT:
                self.image = pygame.transform.flip(self.images[18 + (self.charge_time % 3) * 18 + 0 + self.frame / self.animcycle % 2], 1, 0)

        # bullet
        # rock buster
        if pressed_keys[K_z]:
            self.charge_time = self.charge_time + 1
            Bullet(self.rect.center)
            if self.on_floor:
                if self.direction == self.DIRECTION_RIGHT:
                    if pressed_keys[K_RIGHT]:
                        self.images[18 + 10 + (self.charge_time % 3) * 18 + self.frame / self.animcycle % 3]
                    else:
                        self.image = self.images[18 + 9 + (self.charge_time % 3) * 18]
                elif self.direction == self.DIRECTION_LEFT:
                    if pressed_keys[K_LEFT]:
                        self.image = pygame.transform.flip(self.images[18 + 10 + (self.charge_time % 3) * 18 + self.frame / self.animcycle % 3], 1, 0)
                    else:
                        self.image = pygame.transform.flip(self.images[18 + 9 + (self.charge_time % 3) * 18], 1, 0)
            elif self.on_floor == False: # jumping buster
                if self.direction == self.DIRECTION_RIGHT:
                    self.image = self.images[18 + 7 + (self.charge_time % 3) * 18]
                elif self.direction == self.DIRECTION_LEFT:
                    self.image = pygame.transform.flip(self.images[18 + 7 + (self.charge_time % 3) * 18], 1, 0)
        else:
            self.charge_time = 0

        # ジャンプ開始
        if pressed_keys[K_x]:
            if self.on_floor:
                # SLIDING
                if pressed_keys[K_DOWN]:
                    if self.direction == self.DIRECTION_RIGHT:
                        self.image = self.images[18 + 17 + (self.charge_time % 3) * 18]
                        self.fpvx = self.JUMP_SPEED
                    else:
                        self.image = pygame.transform.flip(self.images[18 + 17 + (self.charge_time % 3) * 18], 1, 0)
                        self.fpvx = -self.JUMP_SPEED
                # JUMP
                else:
                    self.fpvy = -self.JUMP_SPEED  # 上向きに初速度を与える
                    self.on_floor = False
                    self.jump_count = 1
            elif not self.prev_button and self.jump_count < self.MAX_JUMP_COUNT:
                self.fpvy = -self.JUMP_SPEED
                self.jump_count += 1
            
        # update upeed
        if not self.on_floor:
            self.fpvy += self.GRAVITY  # 下向きに重力をかける
        
        self.collision_x() # X方向の衝突判定処理
        self.collision_y() # Y方向の衝突判定処理
        
        # 浮動小数点の位置を整数座標に戻す
        # スプライトを動かすにはself.rectの更新が必要！
        self.rect.x = int(self.fpx)
        self.rect.y = int(self.fpy)
        
        # ボタンのジャンプキーの状態を記録
        self.prev_button = pressed_keys[K_SPACE]
        
    def collision_x(self):
        """X方向の衝突判定処理"""
        # rockman size
        width = self.rect.width
        height = self.rect.height
        
        # X方向の移動先の座標と矩形を求める
        newx = self.fpx + self.fpvx
        newrect = Rect(newx, self.fpy, width, height)
        
        # ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                if self.fpvx > 0:    # 右に移動中に衝突
                    # めり込まないように調整して速度を0に
                    self.fpx = block.rect.left - width
                    self.fpvx = 0
                elif self.fpvx < 0:  # 左に移動中に衝突
                    self.fpx = block.rect.right
                    self.fpvx = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.fpx = newx
    
    def collision_y(self):
        """Y方向の衝突判定処理"""
        # ロックマンのサイズ
        width = self.rect.width
        height = self.rect.height
        
        # Y方向の移動先の座標と矩形を求める
        newy = self.fpy + self.fpvy
        newrect = Rect(self.fpx, newy, width, height)

        on_floor_flg = False

        # ブロックとの衝突判定
        for block in self.blocks:
            collide = newrect.colliderect(block.rect)
            if collide:  # 衝突するブロックあり
                if self.fpvy > 0: # Hit the top side of the wall
                    # めり込まないように調整して速度を0に
                    self.fpy = block.rect.top - height
                    self.fpvy = 0
                    # 下に移動中に衝突したなら床の上にいる
                    if self.status == self.STATUS_START: self.status = self.STATUS_NORMAL
                    on_floor_flg = True
                    self.on_floor = True
                    self.jump_count = 0  # ジャンプカウントをリセット
                elif self.fpvy < 0: # Hit the bottom side of the wall
                    self.fpy = block.rect.bottom
                    self.fpvy = 0
                break  # 衝突ブロックは1個調べれば十分
            else:
                # 衝突ブロックがない場合、位置を更新
                self.fpy = newy
                # ブロックに1個もヒットしていない

#        if not on_floor_flg:
#            self.on_floor = False

