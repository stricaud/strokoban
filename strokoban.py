#!/usr/bin/python3
import pygame
import time

from levels import *
from Draw import *



pygame.init()

levels = Levels("./data/levels/")


def update_level_buffer(level_buffer, char, from_x, from_y, to_x, to_y):
    level_buffer[to_x][to_y] = char
    return True
        
screen = pygame.display.set_mode((800, 600))
levelbuf = levels.get_level("default", 1)
this_level = levels.make_matrix_from_buf(levelbuf)
strokoban_draw = StrokobanDraw(this_level)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_DOWN:
                strokoban_draw.move_buddy("down")
            if event.key == pygame.K_UP:
                strokoban_draw.move_buddy("up")
            if event.key == pygame.K_LEFT:
                strokoban_draw.move_buddy("left")
            if event.key == pygame.K_RIGHT:
                strokoban_draw.move_buddy("right")

    screen.fill((0, 0, 0))  # Clear screen with black
    
    strokoban_draw.draw_level(screen)

    pygame.display.flip()  # Update the display

    time.sleep(0.3)
    
pygame.quit()

