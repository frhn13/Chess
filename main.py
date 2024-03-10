import time
from tkinter import messagebox
import pygame as pg

from Constants import *
from Board import Board
from Button import Button
from csv_operations import *

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
leaderboard_state = LeaderboardState.MENU
in_game_state = InGameState.GAME_PLAYING
game_setup = True
current_turn = "White"
white_player = ""
black_player = ""
player_entered = ""
winner = ""
player1_rect = pg.Rect(280, 80, 200, 50)
player2_rect = pg.Rect(280, 180, 200, 50)
white_player_active = False
black_player_active = False
player_entered_active = False
white_time = 0
black_time = 0
timer_started = False
pawn_to_upgrade = None

board = None
active_piece = None

# Fonts
main_font = pg.font.SysFont("Futura", 40)
title_font = pg.font.SysFont("Futura", 60)

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
fastest_wins_button_img = pg.transform.scale(pg.image.load("img/fastest_wins_btn.png"), (261, 99))
most_wins_button_img = pg.transform.scale(pg.image.load("img/most_wins_btn.png"), (261, 99))
personal_stats_button_img = pg.transform.scale(pg.image.load("img/personal_stats_btn.png"), (261, 99))
view_personal_stats_button_img = pg.transform.scale(pg.image.load("img/view_personal_stats_btn.png"), (261, 99))

white_rook_button_img = pg.transform.scale(pg.image.load("img/white_rook.jpg"), (100, 100))
white_knight_button_img = pg.transform.scale(pg.image.load("img/white_knight.jpg"), (100, 100))
white_bishop_button_img = pg.transform.scale(pg.image.load("img/white_bishop.jpg"), (100, 100))
white_queen_button_img = pg.transform.scale(pg.image.load("img/white_queen.jpg"), (100, 100))
black_rook_button_img = pg.transform.scale(pg.image.load("img/black_rook.jpg"), (100, 100))
black_knight_button_img = pg.transform.scale(pg.image.load("img/black_knight.jpg"), (100, 100))
black_bishop_button_img = pg.transform.scale(pg.image.load("img/black_bishop.jpg"), (100, 100))
black_queen_button_img = pg.transform.scale(pg.image.load("img/black_queen.jpg"), (100, 100))

# Make the sprite groups
all_sprites = pg.sprite.Group()
chess_pieces_sprites = pg.sprite.Group()

# Buttons
start_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, start_button_img)
leaderboard_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 200, leaderboard_button_img)
exit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, exit_button_img)
play_game_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, play_game_button_img)
main_menu_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 320, main_menu_button_img)
fastest_wins_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, fastest_wins_button_img)
most_wins_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 100, most_wins_button_img)
personal_stats_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 100, personal_stats_button_img)
main_menu_leaderboard_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 100, main_menu_button_img)
leaderboard_menu_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 300, leaderboard_button_img)
view_personal_stats_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, view_personal_stats_button_img)
personal_stats_leaderboard_menu_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, leaderboard_button_img)

white_rook_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200, white_rook_button_img)
white_knight_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 200, white_knight_button_img)
white_bishop_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 200, white_bishop_button_img)
white_queen_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 200, white_queen_button_img)
black_rook_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 200, black_rook_button_img)
black_knight_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 200, black_knight_button_img)
black_bishop_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 200, black_bishop_button_img)
black_queen_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 200, black_queen_button_img)

create_file()

while running:
    clock.tick(FPS)
    if game_state == GameState.MAIN_MENU:
        white_time = 0
        black_time = 0
        draw_bg(MENU_BG)
        white_player = ""
        black_player = ""
        player_entered = ""
        winner = ""
        white_player_active = False
        black_player_active = False
        player_entered_active = False
        if start_button.display(screen):
            game_state = GameState.USERNAMES
        if leaderboard_button.display(screen):
            game_state = GameState.LEADERBOARD
        if exit_button.display(screen):
            running = False

    if game_state == GameState.LEADERBOARD:
        if leaderboard_state == LeaderboardState.MENU:
            draw_bg(MENU_BG)
            if fastest_wins_button.display(screen):
                leaderboard_state = LeaderboardState.FASTEST_WINS
            if most_wins_button.display(screen):
                leaderboard_state = LeaderboardState.MOST_WINS
            if personal_stats_button.display(screen):
                leaderboard_state = LeaderboardState.ENTER_PERSONAL_STATS
            if main_menu_leaderboard_button.display(screen):
                game_state = GameState.MAIN_MENU
                leaderboard_state = LeaderboardState.MENU

        if leaderboard_state == LeaderboardState.FASTEST_WINS:
            draw_bg(MENU_BG)
            fastest_wins_list = fastest_wins()
            write_text(SCREEN_WIDTH//2 - 200, 50, f"Top {len(fastest_wins_list)} Fastest Wins", BLACK, title_font)
            for x in range(len(fastest_wins_list)):
                write_text(SCREEN_WIDTH//2 - 200, 150 + (x*100), f"Player: {fastest_wins_list[x][0]}, Time: {fastest_wins_list[x][1]} seconds", BLACK, main_font)
            if leaderboard_menu_button.display(screen):
                leaderboard_state = LeaderboardState.MENU

        if leaderboard_state == LeaderboardState.MOST_WINS:
            draw_bg(MENU_BG)
            most_wins_list = most_wins()
            write_text(SCREEN_WIDTH // 2 - 300, 50, f"Top {len(most_wins_list)} Players with Most Wins", BLACK, title_font)
            for x in range(len(most_wins_list)):
                write_text(SCREEN_WIDTH // 2 - 200, 150 + (x * 100),
                           f"Player: {most_wins_list[x][0]}, Wins: {most_wins_list[x][1]}", BLACK,
                           main_font)
            if leaderboard_menu_button.display(screen):
                leaderboard_state = LeaderboardState.MENU

        if leaderboard_state == LeaderboardState.ENTER_PERSONAL_STATS:
            draw_bg(MENU_BG)
            pg.draw.rect(screen, WHITE, player1_rect)
            write_text(100, 100, f"Enter Player: {player_entered}", BLACK, main_font)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(event.pos):
                        player_entered_active = True
                    else:
                        player_entered_active = False
                if event.type == pg.KEYDOWN:
                    # Can only be alphanumeric
                    if event.key == pg.K_ESCAPE:
                        running = False
                    elif (97 <= event.key <= 122 or 48 <= event.key <= 57) and player_entered_active and len(
                            player_entered) < 10:
                        player_entered += event.unicode
                    elif event.key == pg.K_BACKSPACE:
                        if player_entered_active:
                            player_entered = player_entered[:-1]
            if view_personal_stats_button.display(screen):
                if len(player_entered) > 0:
                    leaderboard_state = LeaderboardState.PERSONAL_STATS
                else:
                    messagebox.showerror("Details Invalid", "Please enter a player name")
            if personal_stats_leaderboard_menu_button.display(screen):
                player_entered = ""
                player_entered_active = False
                leaderboard_state = LeaderboardState.MENU

        if leaderboard_state == LeaderboardState.PERSONAL_STATS:
            draw_bg(MENU_BG)
            num_wins, num_losses, num_stalemates, fastest_win = personal_stats(player_entered)
            write_text(SCREEN_WIDTH // 2 - 150, 50, f"{player_entered}'s Statistics", BLACK, title_font)
            try:
                write_text(SCREEN_WIDTH // 2 - 150, 150, f"Number of Wins: {num_wins[0]}", BLACK,
                           main_font)
            except IndexError:
                write_text(SCREEN_WIDTH // 2 - 150, 150, f"Number of Wins: 0", BLACK, main_font)
            try:
                write_text(SCREEN_WIDTH // 2 - 150, 250, f"Number of Losses: {num_losses[0]}", BLACK,
                           main_font)
            except IndexError:
                write_text(SCREEN_WIDTH // 2 - 150, 250, f"Number of Losses: 0", BLACK, main_font)
            try:
                write_text(SCREEN_WIDTH // 2 - 150, 350, f"Number of Stalemates: {num_stalemates[0]}", BLACK,
                           main_font)
            except IndexError:
                write_text(SCREEN_WIDTH // 2 - 150, 350, f"Number of Stalemates: 0", BLACK, main_font)
            try:
                write_text(SCREEN_WIDTH // 2 - 150, 450, f"Fastest Win: {fastest_win[0][1]} seconds", BLACK,
                           main_font)
            except IndexError:
                write_text(SCREEN_WIDTH // 2 - 150, 450, "Fastest Win: None", BLACK, main_font)
            if leaderboard_menu_button.display(screen):
                player_entered = ""
                player_entered_active = False
                leaderboard_state = LeaderboardState.ENTER_PERSONAL_STATS

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
                    elif white_player_active or black_player_active:
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

    if game_state == GameState.IN_GAME:
        if in_game_state == InGameState.UPGRADE_PAWN:
            draw_bg(GAME_BG)
            write_text(SCREEN_WIDTH // 2 - 300, 50, "Choose piece to upgrade pawn to", BLACK, title_font)
            if current_turn == "Black":
                if white_rook_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.ROOK)
                    in_game_state = InGameState.GAME_PLAYING
                if white_knight_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.KNIGHT)
                    in_game_state = InGameState.GAME_PLAYING
                if white_bishop_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.BISHOP)
                    in_game_state = InGameState.GAME_PLAYING
                if white_queen_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.QUEEN)
                    in_game_state = InGameState.GAME_PLAYING
            else:
                if black_rook_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.ROOK)
                    in_game_state = InGameState.GAME_PLAYING
                if black_knight_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.KNIGHT)
                    in_game_state = InGameState.GAME_PLAYING
                if black_bishop_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.BISHOP)
                    in_game_state = InGameState.GAME_PLAYING
                if black_queen_button.display(screen):
                    board.upgrade_pawn(pawn_to_upgrade, current_turn, ChessPieces.QUEEN)
                    in_game_state = InGameState.GAME_PLAYING

        if in_game_state == InGameState.GAME_PLAYING:
            draw_bg(GAME_BG)
            board.display_board(screen)
            all_sprites.update()
            all_sprites.draw(screen)
            if current_turn == "White":
                write_text(SCREEN_WIDTH//2 - 100, 50, f"{current_turn}'s Turn", WHITE, main_font)
                if not timer_started:
                    start_white_time = time.perf_counter()
                    timer_started = True
            else:
                write_text(SCREEN_WIDTH // 2 - 100, 50, f"{current_turn}'s Turn", BLACK, main_font)
                if not timer_started:
                    start_black_time = time.perf_counter()
                    timer_started = True

    if game_state == GameState.POST_GAME:
        draw_bg(GAME_BG)
        board.display_board(screen)
        all_sprites.draw(screen)
        if winner != "":
            write_text(SCREEN_WIDTH // 2 - 100, 50, f"{winner} wins!", BLACK, main_font)
        else:
            write_text(SCREEN_WIDTH // 2 - 120, 50, f"It's a stalemate!", BLACK, main_font)
        if main_menu_button.display(screen):
            chess_pieces_sprites.empty()
            all_sprites.empty()
            game_state = GameState.MAIN_MENU

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
                what_happened = board.move_piece(active_piece, new_row, new_column, current_turn)
                if what_happened == "Success":
                    old_row = active_piece.row
                    old_column = active_piece.column
                    board.board_contents[new_row][new_column] = active_piece
                    active_piece.row = new_row
                    active_piece.column = new_column
                    active_piece.rect.center = (181 + (62.5 * active_piece.column), 181 + (62.5 * active_piece.row))
                    board.board_contents[old_row][old_column] = None
                    if current_turn == "White":
                        end_white_time = time.perf_counter()
                        white_time += round(end_white_time - start_white_time, 2)
                    else:
                        end_black_time = time.perf_counter()
                        black_time += round(end_black_time - start_black_time, 2)
                    timer_started = False
                    if board.in_checkmate(current_turn):
                        winner = current_turn
                        if current_turn == "White":
                            write_results(white_player, "Yes", round(white_time, 2), black_player, "No", round(black_time, 2))
                        else:
                            write_results(white_player, "No", round(white_time, 2), black_player, "Yes", round(black_time, 2))
                        game_state = GameState.POST_GAME
                    if board.in_stalemate(current_turn):
                        game_state = GameState.POST_GAME
                        write_results(white_player, "Draw", white_time, black_player, "Draw", black_time)
                    if active_piece.piece_type == ChessPieces.PAWN:
                        if current_turn == "White" and new_row == 0 or current_turn == "Black" and new_row == 7:
                            pawn_to_upgrade = active_piece
                            in_game_state = InGameState.UPGRADE_PAWN
                    current_turn = "White" if current_turn == "Black" else "Black"
                if what_happened == "Failed":
                    active_piece.rect.center = (181 + (62.5 * active_piece.column), 181 + (62.5 * active_piece.row))
                active_piece = None

    pg.display.update()

pg.quit()
