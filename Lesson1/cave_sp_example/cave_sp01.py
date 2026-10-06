# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 10:58:13 2022

@author: inoue
"""
import sys
import pygame
from pygame.locals import QUIT, Rect, K_SPACE

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

class MyShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("ship.png")
        self.rect = self.image.get_rect()
        self.rect.y = 250
        self.velocity = 0
    
    def update(self):
        key = pygame.key.get_pressed()
        
        if key[K_SPACE]:
            self.velocity -= 3
        else:
            self.velocity += 3
        
        self.rect.move_ip(0, self.velocity)
        
    def draw(self):
        SURFACE.blit(self.image, self.rect.topleft)

def main():

    my_ship = MyShip()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        SURFACE.fill((0, 255, 0))
        
        my_ship.update()
        my_ship.draw()

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()


