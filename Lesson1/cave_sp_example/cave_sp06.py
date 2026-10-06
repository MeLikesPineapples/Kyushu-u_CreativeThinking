# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:20:39 2022

@author: inoue
"""
import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, K_SPACE, K_RIGHT, K_LEFT

pygame.init()
pygame.key.set_repeat(5, 5)
W = 800
H = 600
SURFACE = pygame.display.set_mode((W, H))
FPSCLOCK = pygame.time.Clock()

class MyShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        self.rect.y = 200
        self.velocity = 0
        self.vx = 0
    
    def update(self):
        key = pygame.key.get_pressed()
        
        if key[K_SPACE]:
            self.velocity -= 3
        else:
            self.velocity += 3
        
        if key[K_RIGHT]:
            self.vx = 5
        elif key[K_LEFT]:
            self.vx = -5
        else:
            self.vx = 0
        
        self.rect.move_ip(self. vx, self.velocity)
        self.rect.clamp_ip(SURFACE.get_rect())
    
    def draw(self):
        SURFACE.blit(self.image, self.rect.topleft)

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect((0,0), (10, H))

class Takoyaki(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("takoyaki.png")
        img_rect = img.get_rect()
        self.image = pygame.transform.rotozoom(img, 0, 20.0/img_rect.w)
        self.rect = self.image.get_rect()
        self.rect.x = randint(W, 2*W)
        self.rect.y = -randint(0, H)
    
    def update(self):
        self.rect.x -= 10
        self.rect.y += 5
        if self.rect.x < -20 or self.rect.y > H:
            self.rect.x = randint(W, 2*W)
            self.rect.y = -randint(0, H)
    
    def draw(self):
        SURFACE.blit(self.image, self.rect.topleft)

def main():
    walls = 80
    score = 0
    slope = randint(1, 6)
    sysfont = pygame.font.SysFont(None, 36)
    bang_image = pygame.image.load("bang.png")
    
    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))
    game_over = False

    my_ship = MyShip()
    
    C_group = pygame.sprite.Group()
    F_group = pygame.sprite.Group()
    
    for _ in range(walls):
        C_group.add(Barrier())
        F_group.add(Barrier())
    
    for i, x in enumerate(C_group.sprites()):
        x.rect = Rect((holes[i].left, 0), (10, holes[i].top))
    for i, x in enumerate(F_group.sprites()):
        x.rect = Rect((holes[i].left, 0), (10, H - holes[i].bottom))
    
    T_group = pygame.sprite.Group()
    
    for _ in range(10):
        T_group.add(Takoyaki())
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        if not game_over:
            score += 10

            edge = holes[-1].copy()
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20)
            edge.move_ip(10, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10, 0) for x in holes]
            
            for i, x in enumerate(C_group.sprites()):
                x.rect.bottom = holes[i].top
            for i, x in enumerate(F_group.sprites()):
                x.rect.top = holes[i].bottom
            
            my_ship.update()
            T_group.update()
            
            if pygame.sprite.spritecollide(my_ship, C_group, False) or \
                pygame.sprite.spritecollide(my_ship, F_group, False):
                game_over = True
            
            if pygame.sprite.spritecollide(my_ship, T_group, True):
                holes[-1].inflate_ip(0, 20)
                T_group.add(Takoyaki())
        
        SURFACE.fill((0, 255, 0))
        
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
                
        my_ship.draw()
        T_group.draw(SURFACE)
        
        score_image = sysfont.render("score is {}".format(score), True, (0, 0, 225))
        SURFACE.blit(score_image, (600, 20))
        
        if game_over:
            SURFACE.blit(bang_image, (my_ship.rect.left, my_ship.rect.top - 40))

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()


