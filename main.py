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
game_setup = True
current_turn = "White"

board = None

while running:
    clock.tick(FPS)
    if game_setup:
        board = Board()
        current_turn = "White"
        board.print_board()
        game_setup = False
    if not game_setup:
        current_pos = input("Choose the coordinates of the piece you want: ")
        next_pos = input("Choose the coordinates to place at: ")
        what_happened = board.move_piece(board.board_contents[int(current_pos[0])][int(current_pos[1])],
                                                    int(current_pos[0]), int(current_pos[1]), int(next_pos[0]),
                                                    int(next_pos[1]), current_turn)
        current_turn = "Black" if current_turn == "White" else "White"
        board.print_board()
        if what_happened == "GameOver":
            print(f"{current_turn} won")
            game_setup = True
        elif what_happened == "GameDrew":
            print("Game was a draw")
            game_setup = True
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
