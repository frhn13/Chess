import pygame as pg

from Constants import *
from Board import Board

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Chess")

# Set the frame rate
clock = pg.time.Clock()

# Game variables
running = True

board = Board()
board.print_board()

while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
