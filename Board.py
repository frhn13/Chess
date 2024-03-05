import pygame as pg
from Piece import Piece
from Constants import *


class Board:
    def __init__(self, x, y, image, pieces_images):
        self.board_contents = []
        self.setup_board(pieces_images)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def display_board(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def setup_board(self, pieces_images):
        for x in range(8):
            row = []
            for y in range(8):
                row.append(None)
            self.board_contents.append(row)
        for x in range(8):
            colour = ""
            if x == 0 or x == 1:
                colour = "Black"
                image_pos = 1
            elif x == 6 or x == 7:
                colour = "White"
                image_pos = 0
            if x == 0 or x == 7:
                self.board_contents[x][0] = Piece("Rook", colour, x, 0, pieces_images[image_pos][1])
                self.board_contents[x][1] = Piece("Knight", colour, x, 1, pieces_images[image_pos][2])
                self.board_contents[x][2] = Piece("Bishop", colour, x, 2, pieces_images[image_pos][3])
                self.board_contents[x][3] = Piece("Queen", colour, x, 3, pieces_images[image_pos][4])
                self.board_contents[x][4] = Piece("King", colour, x, 4, pieces_images[image_pos][5])
                self.board_contents[x][5] = Piece("Bishop", colour, x, 5, pieces_images[image_pos][3])
                self.board_contents[x][6] = Piece("Knight", colour, x, 6, pieces_images[image_pos][2])
                self.board_contents[x][7] = Piece("Rook", colour, x, 7, pieces_images[image_pos][1])
            elif x == 1 or x == 6:
                self.board_contents[x][0] = Piece("Pawn", colour, x, 0, pieces_images[image_pos][0])
                self.board_contents[x][1] = Piece("Pawn", colour, x, 1, pieces_images[image_pos][0])
                self.board_contents[x][2] = Piece("Pawn", colour, x, 2, pieces_images[image_pos][0])
                self.board_contents[x][3] = Piece("Pawn", colour, x, 3, pieces_images[image_pos][0])
                self.board_contents[x][4] = Piece("Pawn", colour, x, 4, pieces_images[image_pos][0])
                self.board_contents[x][5] = Piece("Pawn", colour, x, 5, pieces_images[image_pos][0])
                self.board_contents[x][6] = Piece("Pawn", colour, x, 6, pieces_images[image_pos][0])
                self.board_contents[x][7] = Piece("Pawn", colour, x, 7, pieces_images[image_pos][0])

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
        if piece is None:
            return "NA"
        # if self.in_checkmate(current_turn):
        #     return "GameOver"
        if piece.colour != current_turn:
            return "Failed"
        elif self.board_contents[new_row][new_column] is not None and self.board_contents[new_row][new_column].colour == piece.colour:
            return "Failed"
        elif not piece.is_move_valid(new_row, new_column, self.board_contents[new_row][new_column], self.board_contents):
            return "Failed"
        elif self.in_check(current_turn) and piece.piece_type != "King":
            return "Failed"
        elif self.will_be_in_check(current_turn, new_row, new_column) and piece.piece_type == "King":
            return "Failed"
        # elif self.in_stalemate(current_turn):
        #     return False, "GameDrew"
        else:
            if self.board_contents[new_row][new_column] is not None and self.board_contents[new_row][new_column].colour != piece.colour:
                self.board_contents[new_row][new_column].kill()
            return "Success"

    def in_check(self, current_turn):
        for x in range(len(self.board_contents)):
            for y in range(len(self.board_contents[0])):
                if self.board_contents[x][y] is not None and self.board_contents[x][y].piece_type == "King" \
                        and self.board_contents[x][y].colour == current_turn:
                    for i in range(len(self.board_contents)):
                        for j in range(len(self.board_contents[0])):
                            if self.board_contents[i][j] is not None and \
                                    self.board_contents[i][j].colour != self.board_contents[x][y].colour \
                                    and self.board_contents[i][j].is_move_valid(
                                    x, y, self.board_contents[x][y], self.board_contents):
                                return True
        return False

    def will_put_king_in_check(self, current_turn):
        for x in range(len(self.board_contents)):
            for y in range(len(self.board_contents[0])):
                if self.board_contents[x][y] is not None and self.board_contents[x][y].piece_type == "King" \
                        and self.board_contents[x][y].colour == current_turn:
                    for i in range(len(self.board_contents)):
                        for j in range(len(self.board_contents[0])):
                            if self.board_contents[i][j] is not None and \
                                    self.board_contents[i][j].colour != self.board_contents[x][y].colour \
                                    and self.board_contents[i][j].is_move_valid(
                                    x, y, self.board_contents[x][y], self.board_contents):
                                return True
        return False

    def will_be_in_check(self, current_turn, new_row, new_column):
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != current_turn and \
                        self.board_contents[i][j].is_move_valid(
                            new_row, new_column, self.board_contents[new_row][new_column], self.board_contents):
                    return True
        return False

    def in_checkmate(self, current_turn):
        next_turn = "White" if current_turn == "Black" else "Black"
        # if not self.in_check(next_turn):
        #     print("Yay")
        #     return False
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].piece_type == "King" and \
                        self.board_contents[i][j].colour == current_turn:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            try:
                                if not self.will_be_in_check(current_turn, i+x, j+y) or \
                                    (self.board_contents[i+x][j+y] is not None and
                                     self.board_contents[i+x][j+y].colour != self.board_contents[i][j].colour):
                                    return False
                            except IndexError:
                                pass
        return True

    def in_stalemate(self, current_turn):
        if self.in_check(current_turn):
            return False
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and \
                        self.board_contents[i][j].piece_type == "King" and \
                        self.board_contents[i][j].colour == current_turn:
                    for x in range(-1, 2):
                        for y in range(-1, 2):
                            try:
                                if not self.will_be_in_check(current_turn, i+x, j+y) or \
                                    (self.board_contents[i+x][j+y] is not None and
                                     self.board_contents[i+x][j+y].colour != self.board_contents[i][j].colour):
                                    return False
                            except IndexError:
                                pass
        return True
