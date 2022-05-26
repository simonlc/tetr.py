import pygame
import math
from .screen import screen

red = (255,0,0)
cellSize = math.floor(480 / 20)
skin = pygame.image.load('tetris/skin1.png').convert()

def drawCell(x, y, color, ctx = screen, offset = (0, 0), opacity = 255):
    x = math.floor(x * cellSize) + offset[0]
    y = math.floor(y) * cellSize - cellSize * 2 + offset[1]
    if opacity < 255:
        s = pygame.Surface((cellSize, cellSize), pygame.SRCALPHA)
        s.set_alpha(128)
        s.blit(skin, (0, 0), (color * cellSize, 0, cellSize, cellSize))
        screen.blit(s, (x, y))
    else:
        screen.blit(skin, (x, y), (color * cellSize, 0, cellSize, cellSize))

def draw(tetro, cx, cy, ctx, color = None, offset = (0, 0), opacity = 255):
    for x in range(len(tetro)):
        for y in range(len(tetro[x])):
            if tetro[x][y]:
                drawCell(x + cx, y + cy, color if color != None else tetro[x][y], ctx, offset, opacity)
