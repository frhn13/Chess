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
board.move_piece(board.board_contents[1][0], 1, 0, 2, 0)
board.move_piece(board.board_contents[2][0], 2, 0, 3, 0)
board.move_piece(board.board_contents[3][0], 3, 0, 4, 0)
board.move_piece(board.board_contents[0][0], 0, 0, 4, 0)
board.move_piece(board.board_contents[1][1], 1, 1, 2, 1)
board.move_piece(board.board_contents[0][2], 0, 2, 2, 4)
board.move_piece(board.board_contents[0][1], 0, 1, 2, 2)
board.print_board()

while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
