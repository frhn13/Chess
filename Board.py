import pygame as pg
from Piece import Piece
from Constants import *


class Board:
    def __init__(self):
        self.board_contents = []
        self.setup_board()

    def setup_board(self):
        for x in range(8):
            row = []
            for y in range(8):
                row.append(None)
            self.board_contents.append(row)
        for x in range(8):
            colour = ""
            if x == 0 or x == 1:
                colour = "Black"
            elif x == 6 or x == 7:
                colour = "White"
            if x == 0 or x == 7:
                self.board_contents[x][0] = Piece("Rook", colour, x, 0)
                self.board_contents[x][1] = Piece("Knight", colour, x, 1)
                self.board_contents[x][2] = Piece("Bishop", colour, x, 2)
                self.board_contents[x][3] = Piece("Queen", colour, x, 3)
                self.board_contents[x][4] = Piece("King", colour, x, 4)
                self.board_contents[x][5] = Piece("Bishop", colour, x, 5)
                self.board_contents[x][6] = Piece("Knight", colour, x, 6)
                self.board_contents[x][7] = Piece("Rook", colour, x, 7)
            elif x == 1 or x == 6:
                self.board_contents[x][0] = Piece("Pawn", colour, x, 0)
                self.board_contents[x][1] = Piece("Pawn", colour, x, 1)
                self.board_contents[x][2] = Piece("Pawn", colour, x, 2)
                self.board_contents[x][3] = Piece("Pawn", colour, x, 3)
                self.board_contents[x][4] = Piece("Pawn", colour, x, 4)
                self.board_contents[x][5] = Piece("Pawn", colour, x, 5)
                self.board_contents[x][6] = Piece("Pawn", colour, x, 6)
                self.board_contents[x][7] = Piece("Pawn", colour, x, 7)

    def print_board(self):
        for x in range(len(self.board_contents)):
            for y in range(len(self.board_contents[0])):
                if self.board_contents[x][y] is not None:
                    print(f"Piece: {self.board_contents[x][y].piece_type}, Colour: {self.board_contents[x][y].colour}", end="; ")
                else:
                    print("None", end=", ")
            print("")
        print("")

    def move_piece(self, piece, current_row, current_column, new_row, new_column, current_turn):
        if piece.colour != current_turn:
            return False
        if self.board_contents[new_row][new_column] is not None and self.board_contents[new_row][new_column].colour == piece.colour:
            return False
        elif not piece.is_move_valid(new_row, new_column, self.board_contents[new_row][new_column], self.board_contents):
            return False
        else:
            if self.board_contents[new_row][new_column] is not None and self.board_contents[new_row][new_column].colour != piece.colour:
                piece.kill()
            self.board_contents[new_row][new_column] = piece
            piece.row = new_row
            piece.column = new_column
            self.board_contents[current_row][current_column] = None
            return True
