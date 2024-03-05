import pygame as pg

from Constants import *
from Board import Board

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Chess")


def draw_bg(colour):
    screen.fill(colour)


# Set the frame rate
clock = pg.time.Clock()

# Game variables
running = True
game_setup = True
current_turn = "White"

board = None
active_piece = None

# Images
board_img = pg.transform.scale(pg.image.load("img/chess_board.jpg"), (500, 500))
white_pawn_img = pg.transform.scale(pg.image.load("img/white_pawn.jpg"), (45, 45))
white_rook_img = pg.transform.scale(pg.image.load("img/white_rook.jpg"), (45, 45))
white_knight_img = pg.transform.scale(pg.image.load("img/white_knight.jpg"), (45, 45))
white_bishop_img = pg.transform.scale(pg.image.load("img/white_bishop.jpg"), (45, 45))
white_queen_img = pg.transform.scale(pg.image.load("img/white_queen.jpg"), (45, 45))
white_king_img = pg.transform.scale(pg.image.load("img/white_king.jpg"), (45, 45))

black_pawn_img = pg.transform.scale(pg.image.load("img/black_pawn.jpg"), (45, 45))
black_rook_img = pg.transform.scale(pg.image.load("img/black_rook.jpg"), (45, 45))
black_knight_img = pg.transform.scale(pg.image.load("img/black_knight.jpg"), (45, 45))
black_bishop_img = pg.transform.scale(pg.image.load("img/black_bishop.jpg"), (45, 45))
black_queen_img = pg.transform.scale(pg.image.load("img/black_queen.jpg"), (45, 45))
black_king_img = pg.transform.scale(pg.image.load("img/black_king.jpg"), (45, 45))

pieces_images = [[white_pawn_img, white_rook_img, white_knight_img, white_bishop_img, white_queen_img, white_king_img],
                 [black_pawn_img, black_rook_img, black_knight_img, black_bishop_img, black_queen_img, black_king_img]]

all_sprites = pg.sprite.Group()
chess_pieces_sprites = pg.sprite.Group()

while running:
    clock.tick(FPS)
    if game_setup:
        board = Board(400, 400, board_img, pieces_images)
        for x in range(len(board.board_contents)):
            for y in range(len(board.board_contents[0])):
                if x == 1 or x == 0 or x == 6 or x == 7:
                    all_sprites.add(board.board_contents[x][y])
                    chess_pieces_sprites.add(board.board_contents[x][y])
        current_turn = "White"
        board.print_board()
        game_setup = False
    if not game_setup:
        draw_bg(GAME_BG)
        board.display_board(screen)
        all_sprites.update()
        all_sprites.draw(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            pos = pg.mouse.get_pos()
            for piece in chess_pieces_sprites:
                if piece.rect.collidepoint(event.pos):
                    active_piece = piece

        if event.type == pg.MOUSEMOTION:
            pos = pg.mouse.get_pos()
            if active_piece != None:
                active_piece.rect.center = (pos[0], pos[1])

        if event.type == pg.MOUSEBUTTONUP:
            active_piece = None

    pg.display.update()

pg.quit()
