from tkinter import messagebox
import pygame as pg

from Constants import *
from Board import Board
from Button import Button

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Chess")


def draw_bg(colour):
    screen.fill(colour)


def write_text(text_x, text_y, contents, colour, font):
    text = font.render(contents, True, colour)
    screen.blit(text, (text_x, text_y))


# Set the frame rate
clock = pg.time.Clock()

# Game variables
running = True
game_state = GameState.MAIN_MENU
game_setup = True
current_turn = "White"
white_player = ""
black_player = ""
player1_rect = pg.Rect(280, 80, 200, 50)
player2_rect = pg.Rect(280, 180, 200, 50)
white_player_active = False
black_player_active = False

board = None
active_piece = None

# Fonts
main_font = pg.font.SysFont("Futura", 40)

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

start_button_img = pg.transform.scale(pg.image.load("img/start_btn.png"), (261, 99))
leaderboard_button_img = pg.transform.scale(pg.image.load("img/leaderboard_btn.png"), (261, 99))
exit_button_img = pg.transform.scale(pg.image.load("img/exit_btn.png"), (261, 99))
main_menu_button_img = pg.transform.scale(pg.image.load("img/menu_btn.png"), (261, 99))
play_game_button_img = pg.transform.scale(pg.image.load("img/play_game_btn.png"), (261, 99))

# Make the sprite groups
all_sprites = pg.sprite.Group()
chess_pieces_sprites = pg.sprite.Group()

# Buttons
start_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, start_button_img)
leaderboard_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200, leaderboard_button_img)
exit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, exit_button_img)
play_game_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, play_game_button_img)
main_menu_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300, main_menu_button_img)

while running:
    clock.tick(FPS)
    if game_state == GameState.MAIN_MENU:
        draw_bg(MENU_BG)
        white_player = ""
        black_player = ""
        white_player_active = False
        black_player_active = False
        if start_button.display(screen):
            game_state = GameState.USERNAMES
        if leaderboard_button.display(screen):
            game_state = GameState.LEADERBOARD
        if exit_button.display(screen):
            running = False

    if game_state == GameState.LEADERBOARD:
        game_state = GameState.MAIN_MENU

    if game_state == GameState.USERNAMES:
        draw_bg(MENU_BG)
        pg.draw.rect(screen, WHITE, player1_rect)
        pg.draw.rect(screen, WHITE, player2_rect)
        write_text(100, 100, f"White Player: {white_player}", BLACK, main_font)
        write_text(100, 200, f"Black Player: {black_player}", BLACK, main_font)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if player1_rect.collidepoint(event.pos):
                    white_player_active = True
                    black_player_active = False
                elif player2_rect.collidepoint(event.pos):
                    white_player_active = False
                    black_player_active = True
                else:
                    white_player_active = False
                    black_player_active = False
            if event.type == pg.KEYDOWN:
                # Can only be alphanumeric
                if event.key == pg.K_ESCAPE:
                    running = False
                elif (97 <= event.key <= 122 or 48 <= event.key <= 57) and white_player_active and len(white_player) < 10:
                    white_player += event.unicode
                elif (97 <= event.key <= 122 or 48 <= event.key <= 57) and black_player_active and len(black_player) < 10:
                    black_player += event.unicode
                elif event.key == pg.K_BACKSPACE:
                    if white_player_active:
                        white_player = white_player[:-1]
                    elif black_player_active:
                        black_player = black_player[:-1]
                else:
                    if (white_player_active and len(white_player) == 10) or (black_player_active and len(black_player) == 10):
                        messagebox.showerror("Details invalid", "Player name can't be more than 10 characters")
                    else:
                        messagebox.showerror("Details invalid", "Player name can only contain numbers or letters")
        if play_game_button.display(screen):
            if white_player == black_player:
                messagebox.showerror("Same details", "Both players can't have the same name")
            if len(white_player) < 4 or len(black_player) < 4:
                messagebox.showerror("Details invalid", "Player name can't be less than 4 characters")
            else:
                game_state = GameState.GAME_SETUP
        if main_menu_button.display(screen):
            game_state = GameState.MAIN_MENU

    if game_state == GameState.GAME_SETUP:
        board = Board(400, 400, board_img, pieces_images)
        for x in range(len(board.board_contents)):
            for y in range(len(board.board_contents[0])):
                if x == 1 or x == 0 or x == 6 or x == 7:
                    all_sprites.add(board.board_contents[x][y])
                    chess_pieces_sprites.add(board.board_contents[x][y])
        current_turn = "White"
        game_state = GameState.IN_GAME

    if game_state == GameState.POST_GAME:
        game_state = GameState.MAIN_MENU

    if game_state == GameState.IN_GAME:
        draw_bg(GAME_BG)
        board.display_board(screen)
        all_sprites.update()
        all_sprites.draw(screen)
        if current_turn == "White":
            write_text(SCREEN_WIDTH//2 - 100, 50, f"{current_turn}'s Turn", WHITE, main_font)
        else:
            write_text(SCREEN_WIDTH // 2 - 100, 50, f"{current_turn}'s Turn", BLACK, main_font)

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
            if active_piece is not None:
                active_piece.rect.center = (pos[0], pos[1])

        if event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            new_row = int(round((pos[1] - 181) / 62.5, 0))
            new_column = int(round((pos[0] - 181) / 62.5, 0))
            if active_piece is not None:
                what_happened = board.move_piece(active_piece, active_piece.row, active_piece.column, new_row, new_column, current_turn)
                if what_happened == "Success":
                    old_row = active_piece.row
                    old_column = active_piece.column
                    board.board_contents[new_row][new_column] = active_piece
                    active_piece.row = new_row
                    active_piece.column = new_column
                    active_piece.rect.center = (181 + (62.5 * active_piece.column), 181 + (62.5 * active_piece.row))
                    board.board_contents[old_row][old_column] = None
                    if board.in_checkmate(current_turn):
                        chess_pieces_sprites.empty()
                        all_sprites.empty()
                        game_state = GameState.POST_GAME
                        print(f"{current_turn} wins!")
                    if board.in_stalemate(current_turn):
                        chess_pieces_sprites.empty()
                        all_sprites.empty()
                        game_state = GameState.POST_GAME
                        print("It is a draw!")
                    if active_piece.piece_type == "Pawn":
                        if current_turn == "White" and new_row == 0 or current_turn == "Black" and new_row == 7:
                            board.upgrade_pawn(active_piece, current_turn)
                    current_turn = "White" if current_turn == "Black" else "Black"
                if what_happened == "Failed":
                    active_piece.rect.center = (181 + (62.5 * active_piece.column), 181 + (62.5 * active_piece.row))
                active_piece = None

    pg.display.update()

pg.quit()
