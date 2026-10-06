# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 16:56:40 2022

@author: inoue
"""
import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, K_SPACE

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
    
    def update(self):
        key = pygame.key.get_pressed()
        
        if key[K_SPACE]:
            self.velocity -= 3
        else:
            self.velocity += 3
        
        self.rect.move_ip(0, self.velocity)
    
    def draw(self):
        SURFACE.blit(self.image, self.rect.topleft)

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = Rect((0,0), (10, H))

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
            
            if pygame.sprite.spritecollide(my_ship, C_group, False) or \
                pygame.sprite.spritecollide(my_ship, F_group, False):
                game_over = True
        
        SURFACE.fill((0, 255, 0))
        
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
                
        my_ship.draw()
        
        score_image = sysfont.render("score is {}".format(score), True, (0, 0, 225))
        SURFACE.blit(score_image, (600, 20))
        
        if game_over:
            SURFACE.blit(bang_image, (0, my_ship.rect.top - 40))

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()


