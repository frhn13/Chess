from enum import Enum

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
CHESS_PIECES = ["Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]

# Colours
GAME_BG = (144, 201, 120)
MENU_BG = (255, 192, 203)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class GameState(Enum):
    MAIN_MENU = 1
    USERNAMES = 2
    LEADERBOARD = 3
    GAME_SETUP = 4
    IN_GAME = 5
    POST_GAME = 6
