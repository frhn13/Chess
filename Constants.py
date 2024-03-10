from enum import Enum

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60

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


class LeaderboardState(Enum):
    MENU = 1
    MOST_WINS = 2
    FASTEST_WINS = 3
    ENTER_PERSONAL_STATS = 4
    PERSONAL_STATS = 5


class InGameState(Enum):
    GAME_PLAYING = 1
    UPGRADE_PAWN = 2


class ChessPieces(Enum):
    ROOK = 1
    KNIGHT = 2
    BISHOP = 3
    QUEEN = 4
    KING = 5
    PAWN = 6
