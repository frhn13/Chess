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
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.no_white_pieces = 16
        self.no_black_pieces = 16

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
                    print(f"Piece: {self.board_contents[x][y].piece_type}, Colour: {self.board_contents[x][y].colour}",
                          end="; ")
                else:
                    print("None", end=", ")
            print("")
        print("")

    def move_piece(self, piece, current_row, current_column, new_row, new_column, current_turn):
        try:
            if piece is None:
                return "NA"
            if piece.colour != current_turn:
                return "Failed"
            elif self.board_contents[new_row][new_column] is not None and \
                    self.board_contents[new_row][new_column].colour == piece.colour:
                return "Failed"
            elif not piece.is_move_valid(new_row, new_column, self.board_contents[new_row][new_column],
                                         self.board_contents):
                return "Failed"
            elif self.in_check(current_turn, piece, new_row, new_column):
                return "Failed"
            elif self.will_be_in_check(current_turn, new_row, new_column) and piece.piece_type == "King":
                return "Failed"
            elif self.will_put_king_in_check(piece, new_row, new_column, current_turn) and piece.piece_type != "King":
                return "Failed"
            #elif self.in_stalemate(current_turn):
            #    return "GameDrew"
            else:
                if self.board_contents[new_row][new_column] is not None and \
                        self.board_contents[new_row][new_column].colour != piece.colour:
                    self.board_contents[new_row][new_column].kill()
                    if piece.colour == "Black":
                        self.no_white_pieces -= 1
                    else:
                        self.no_black_pieces -= 1
                if piece.piece_type == "King":
                    if piece.colour == "White":
                        self.white_king_pos = (new_row, new_column)
                    else:
                        self.black_king_pos = (new_row, new_column)
                return "Success"
        except IndexError:
            return "Failed"

    def in_check(self, current_turn, piece, new_row, new_column):
        no_checking_pieces = 0
        checking_pieces = []
        if current_turn == "White":
            x = self.white_king_pos[0]
            y = self.white_king_pos[1]
        else:
            x = self.black_king_pos[0]
            y = self.black_king_pos[1]
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != \
                        self.board_contents[x][y].colour and self.board_contents[i][j].is_move_valid(
                        x, y, self.board_contents[x][y], self.board_contents):
                    no_checking_pieces += 1
                    checking_pieces.append([i, j])
        print(checking_pieces)
        print(new_row)
        print(new_column)
        if no_checking_pieces == 0:
            return False
        if no_checking_pieces > 1 and piece.piece_type != "King":
            return True
        if piece.piece_type == "King":
            return self.will_be_in_check(current_turn, new_row, new_column)
        if no_checking_pieces == 1:
            if x == checking_pieces[0][0] and y != checking_pieces[0][1]:
                if new_row == x:
                    return False
            if x != checking_pieces[0][0] and y == checking_pieces[0][1]:
                if new_column == y:
                    return False
            if x != checking_pieces[0][0] and y != checking_pieces[0][1]:
                if abs(x - new_row) == abs(y - new_column):
                    if x > checking_pieces[0][0] and y > checking_pieces[0][1] and checking_pieces[0][0] < new_row < x \
                            and checking_pieces[0][1] < new_column < y:
                        return False
                    if x > checking_pieces[0][0] and y < checking_pieces[0][1] and checking_pieces[0][0] < new_row < x \
                            and y < new_column < checking_pieces[0][1]:
                        return False
                    if x < checking_pieces[0][0] and y > checking_pieces[0][1] and x < new_row < checking_pieces[0][0] \
                            and checking_pieces[0][1] < new_column < y:
                        return False
                    if x < checking_pieces[0][0] and y < checking_pieces[0][1] and x < new_row < checking_pieces[0][0] \
                            and y < new_column < checking_pieces[0][1]:
                        return False
            if new_row == checking_pieces[0][0] and new_column == checking_pieces[0][1]:
                return False
            else:
                return True

    def will_put_king_in_check(self, piece, new_row, new_column, current_turn):
        if current_turn == "White":
            x = self.white_king_pos[0]
            y = self.white_king_pos[1]
        else:
            x = self.black_king_pos[0]
            y = self.black_king_pos[1]

        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and \
                        self.board_contents[i][j].colour != self.board_contents[x][y].colour \
                        and self.board_contents[i][j].is_move_valid(
                        piece.row, piece.column, self.board_contents[piece.row][piece.column], self.board_contents):
                    if piece.row == x and piece.column != y \
                            and new_row != piece.row and new_row != i and new_column != j and \
                            (self.board_contents[i][j].piece_type == "Rook" or
                             self.board_contents[i][j].piece_type == "Queen"):
                        return True
                    if piece.row != x and piece.column == y \
                            and new_column != piece.column and new_row != i and new_column != j \
                            and (self.board_contents[i][j].piece_type == "Rook" or
                                 self.board_contents[i][j].piece_type == "Queen"):
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

    def will_be_out_of_checkmate(self, piece, new_row, new_column):
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != piece.colour and \
                        self.board_contents[i][j].is_move_valid(
                            new_row, new_column, self.board_contents[new_row][new_column], self.board_contents):
                    return False
        return True

    def in_checkmate(self, current_turn):
        no_checking_pieces = 0
        checking_pieces = []
        if current_turn == "White":
            x = self.black_king_pos[0]
            y = self.black_king_pos[1]
        else:
            x = self.white_king_pos[0]
            y = self.white_king_pos[1]
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != \
                        self.board_contents[x][y].colour and self.board_contents[i][j].is_move_valid(
                        x, y, self.board_contents[x][y], self.board_contents):
                    no_checking_pieces += 1
                    checking_pieces.append([i, j])
        if no_checking_pieces == 0:
            return False
        else:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if self.board_contents[x + i][y + j] is None or (self.board_contents[x + i][x + j] is not None
                                                                         and self.board_contents[x][y].colour !=
                                                                         self.board_contents[x + i][y + j].colour):
                            if self.will_be_out_of_checkmate(self.board_contents[x][y], x + i, y + j):
                                return False
                    except IndexError:
                        continue
        return True

    def in_stalemate(self, current_turn):
        no_checking_pieces = 0
        checking_pieces = []
        if current_turn == "White":
            x = self.black_king_pos[0]
            y = self.black_king_pos[1]
            pieces_left = self.no_black_pieces
        else:
            x = self.white_king_pos[0]
            y = self.white_king_pos[1]
            pieces_left = self.no_white_pieces
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != \
                        self.board_contents[x][y].colour and self.board_contents[i][j].is_move_valid(
                        x, y, self.board_contents[x][y], self.board_contents):
                    no_checking_pieces += 1
                    checking_pieces.append([i, j])
        if no_checking_pieces > 0:
            return False
        elif pieces_left == 1:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        if self.board_contents[x + i][y + j] is None or (self.board_contents[x + i][x + j] is not None
                                                                         and self.board_contents[x][y].colour !=
                                                                         self.board_contents[x + i][y + j].colour):
                            if self.will_be_out_of_checkmate(self.board_contents[x][y], x + i, y + j):
                                return False
                    except IndexError:
                        continue
        else:
            return False
        return True
