from Piece import Piece
from Constants import *


class Board:
    def __init__(self, x, y, image, pieces_images):
        self.board_contents = []
        self.pieces_images = pieces_images
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
                self.board_contents[x][0] = Piece(ChessPieces.ROOK, colour, x, 0, pieces_images[image_pos][1])
                self.board_contents[x][1] = Piece(ChessPieces.KNIGHT, colour, x, 1, pieces_images[image_pos][2])
                self.board_contents[x][2] = Piece(ChessPieces.BISHOP, colour, x, 2, pieces_images[image_pos][3])
                self.board_contents[x][3] = Piece(ChessPieces.QUEEN, colour, x, 3, pieces_images[image_pos][4])
                self.board_contents[x][4] = Piece(ChessPieces.KING, colour, x, 4, pieces_images[image_pos][5])
                self.board_contents[x][5] = Piece(ChessPieces.BISHOP, colour, x, 5, pieces_images[image_pos][3])
                self.board_contents[x][6] = Piece(ChessPieces.KNIGHT, colour, x, 6, pieces_images[image_pos][2])
                self.board_contents[x][7] = Piece(ChessPieces.ROOK, colour, x, 7, pieces_images[image_pos][1])
            elif x == 1 or x == 6:
                self.board_contents[x][0] = Piece(ChessPieces.PAWN, colour, x, 0, pieces_images[image_pos][0])
                self.board_contents[x][1] = Piece(ChessPieces.PAWN, colour, x, 1, pieces_images[image_pos][0])
                self.board_contents[x][2] = Piece(ChessPieces.PAWN, colour, x, 2, pieces_images[image_pos][0])
                self.board_contents[x][3] = Piece(ChessPieces.PAWN, colour, x, 3, pieces_images[image_pos][0])
                self.board_contents[x][4] = Piece(ChessPieces.PAWN, colour, x, 4, pieces_images[image_pos][0])
                self.board_contents[x][5] = Piece(ChessPieces.PAWN, colour, x, 5, pieces_images[image_pos][0])
                self.board_contents[x][6] = Piece(ChessPieces.PAWN, colour, x, 6, pieces_images[image_pos][0])
                self.board_contents[x][7] = Piece(ChessPieces.PAWN, colour, x, 7, pieces_images[image_pos][0])

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

    def upgrade_pawn(self, piece, current_turn, chess_piece):
        piece.piece_type = chess_piece
        piece_colour = 0 if current_turn == "Black" else 1
        piece.image = self.pieces_images[piece_colour][chess_piece.value]

    def move_piece(self, piece, new_row, new_column, current_turn):
        try:
            self.are_pawns_stuck(current_turn)
            if piece is None:
                return "NA"
            if piece.colour != current_turn:
                return "Failed"
            elif self.board_contents[new_row][new_column] is not None and \
                    self.board_contents[new_row][new_column].colour == piece.colour:
                return "Failed"
            elif not piece.is_move_valid(new_row, new_column, self.board_contents[new_row][new_column],
                                         self.board_contents, False):
                return "Failed"
            elif self.in_check(current_turn, piece, new_row, new_column):
                return "Failed"
            elif piece.piece_type == ChessPieces.KING and self.will_be_in_check(current_turn, new_row, new_column):
                return "Failed"
            elif piece.piece_type != ChessPieces.KING and self.will_put_king_in_check(piece, new_row, new_column, current_turn):
                return "Failed"
            else:
                if self.board_contents[new_row][new_column] is not None and \
                        self.board_contents[new_row][new_column].colour != piece.colour:
                    self.board_contents[new_row][new_column].kill()
                    if piece.colour == "Black":
                        self.no_white_pieces -= 1
                    else:
                        self.no_black_pieces -= 1
                if piece.piece_type == ChessPieces.KING:
                    if piece.colour == "White":
                        self.white_king_pos = (new_row, new_column)
                    else:
                        self.black_king_pos = (new_row, new_column)
                piece.has_moved = True
                return "Success"
        except IndexError:
            return "Failed"

    def are_pawns_stuck(self, current_turn):
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].piece_type == ChessPieces.PAWN and self.board_contents[i][j].colour == current_turn:
                    if (current_turn == "White" and self.board_contents[i-1][j] is not None) or (current_turn == "Black" and self.board_contents[i+1][j] is not None):
                        self.board_contents[i][j].is_blocked = True
                    else:
                        self.board_contents[i][j].is_blocked = False

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
                        x, y, self.board_contents[x][y], self.board_contents, False):
                    no_checking_pieces += 1
                    checking_pieces.append([i, j])
        if no_checking_pieces == 0:
            return False
        if no_checking_pieces > 1 and piece.piece_type != ChessPieces.KING:
            return True
        if piece.piece_type == ChessPieces.KING:
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
            king_x = self.white_king_pos[0]
            king_y = self.white_king_pos[1]
        else:
            king_x = self.black_king_pos[0]
            king_y = self.black_king_pos[1]

        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and \
                        self.board_contents[i][j].colour != self.board_contents[king_x][king_y].colour \
                        and self.board_contents[i][j].is_move_valid(
                        piece.row, piece.column, self.board_contents[piece.row][piece.column], self.board_contents, False):
                    if piece.row == king_x and piece.column != king_y and i != king_x and j == king_y \
                            and new_row != piece.row and new_row != i and new_column != j and \
                            (self.board_contents[i][j].piece_type == ChessPieces.ROOK or
                             self.board_contents[i][j].piece_type == ChessPieces.QUEEN):
                        return True
                    if piece.row != king_x and piece.column == king_y and i != king_x and j == king_y \
                            and new_column != piece.column and new_row != i and new_column != j \
                            and (self.board_contents[i][j].piece_type == ChessPieces.ROOK or
                                 self.board_contents[i][j].piece_type == ChessPieces.QUEEN):
                        return True
                    if piece.row == king_x and piece.column != king_y and piece.column < king_y:
                        for pos_y in range(piece.column + 1, king_y):
                            if self.board_contents[king_x][pos_y] is not None:
                                return False
                    if piece.row == king_x and piece.column != king_y and piece.column > king_y:
                        for pos_y in range(king_y + 1, piece.column):
                            if self.board_contents[king_x][pos_y] is not None:
                                return False
                    if piece.row != king_x and piece.column == king_y and piece.row < king_x:
                        for pos_x in range(piece.row + 1, king_x):
                            if self.board_contents[pos_x][king_y] is not None:
                                return False
                    if piece.row != king_x and piece.column == king_y and piece.row > king_x:
                        for pos_x in range(king_x + 1, piece.row):
                            if self.board_contents[pos_x][king_y] is not None:
                                return False
                    if abs(piece.row - king_x) == abs(piece.column - king_y) and abs(piece.row - i) == abs(piece.column - j) \
                            and (new_row != i or new_column != j) and abs(king_x - i) == abs(king_y - j) and \
                            (self.board_contents[i][j].piece_type == ChessPieces.BISHOP or
                             self.board_contents[i][j].piece_type == ChessPieces.QUEEN):
                        if king_x < i and king_y < j:
                            for pos_x in range(king_x + 1, i):
                                for pos_y in range(king_y + 1, j):
                                    if abs(pos_x-king_x) == abs(pos_y-king_y) and ((new_row == pos_x and new_column == pos_y) or
                                                                                   (self.board_contents[pos_x][pos_y] is not None and (piece.row != pos_x or piece.column != pos_y))):
                                        return False
                        if king_x < i and king_y > j:
                            for pos_x in range(king_x + 1, i):
                                for pos_y in range(j+1, king_y):
                                    if abs(pos_x-king_x) == abs(pos_y-king_y) and ((new_row == pos_x and new_column == pos_y) or
                                                                                   (self.board_contents[pos_x][pos_y] is not None and (piece.row != pos_x or piece.column != pos_y))):
                                        return False
                        if king_x > i and king_y < j:
                            for pos_x in range(i+1, king_x):
                                for pos_y in range(king_y + 1, j):
                                    if abs(pos_x-king_x) == abs(pos_y-king_y) and ((new_row == pos_x and new_column == pos_y) or
                                                                                   (self.board_contents[pos_x][pos_y] is not None and (piece.row != pos_x or piece.column != pos_y))):
                                        return False
                        if king_x > i and king_y > j:
                            for pos_x in range(i+1, king_x):
                                for pos_y in range(j+1, king_y):
                                    if abs(pos_x-king_x) == abs(pos_y-king_y) and ((new_row == pos_x and new_column == pos_y) or
                                                                                   (self.board_contents[pos_x][pos_y] is not None and (piece.row != pos_x or piece.column != pos_y))):
                                        return False
                        return True

        return False

    def will_be_in_check(self, current_turn, new_row, new_column):
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != current_turn and \
                        self.board_contents[i][j].is_move_valid(
                            new_row, new_column, self.board_contents[new_row][new_column], self.board_contents, True):
                    return True
        return False

    def will_be_out_of_checkmate(self, piece, new_row, new_column):
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != piece.colour and \
                        self.board_contents[i][j].is_move_valid(
                            new_row, new_column, self.board_contents[new_row][new_column], self.board_contents, False):
                    return False
        return True

    def in_checkmate(self, current_turn):
        no_checking_pieces = 0
        checking_pieces = []
        if current_turn == "White":
            king_x = self.black_king_pos[0]
            king_y = self.black_king_pos[1]
        else:
            king_x = self.white_king_pos[0]
            king_y = self.white_king_pos[1]
        for i in range(len(self.board_contents)):
            for j in range(len(self.board_contents[0])):
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != \
                        self.board_contents[king_x][king_y].colour and self.board_contents[i][j].is_move_valid(
                        king_x, king_y, self.board_contents[king_x][king_y], self.board_contents, False):
                    no_checking_pieces += 1
                    checking_pieces.append([i, j])
        if no_checking_pieces == 0:
            return False
        if no_checking_pieces == 1:
            for i in range(len(self.board_contents)):
                for j in range(len(self.board_contents[0])):
                    if self.board_contents[i][j] is not None and self.board_contents[i][j].colour != self.board_contents[checking_pieces[0][0]][checking_pieces[0][1]].colour and \
                            self.board_contents[i][j].is_move_valid(
                                checking_pieces[0][0], checking_pieces[0][1], self.board_contents[checking_pieces[0][0]][checking_pieces[0][1]], self.board_contents, False):
                        return False
                    if king_x == checking_pieces[0][0] and king_y != checking_pieces[0][1]:
                        if king_y < checking_pieces[0][1]:
                            for pos in range(king_y + 1, checking_pieces[0][1]):
                                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour == self.board_contents[king_x][king_y].colour and \
                                        (self.board_contents[king_x][pos] is None or self.board_contents[i][j].colour != self.board_contents[king_x][pos].colour) and \
                                         self.board_contents[i][j].is_move_valid(king_x, pos, self.board_contents[king_x][pos], self.board_contents, False) and i != king_x and j != king_y:
                                    return False
                        elif king_y > checking_pieces[0][1]:
                            for pos in range(checking_pieces[0][1]+1, king_y):
                                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour == self.board_contents[king_x][king_y].colour and \
                                        (self.board_contents[king_x][pos] is None or self.board_contents[i][j].colour != self.board_contents[king_x][pos].colour) and \
                                        self.board_contents[i][j].is_move_valid(king_x, pos, self.board_contents[king_x][pos], self.board_contents, False) and i != king_x and j != king_y:
                                    return False
                    if king_x != checking_pieces[0][0] and king_y == checking_pieces[0][1]:
                        if king_x < checking_pieces[0][0]:
                            for pos in range(king_x + 1, checking_pieces[0][0]):
                                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour == self.board_contents[king_x][king_y].colour and \
                                        (self.board_contents[pos][king_y] is None or self.board_contents[i][j].colour != self.board_contents[pos][king_y].colour) and \
                                        self.board_contents[i][j].is_move_valid(pos, king_y, self.board_contents[pos][king_y], self.board_contents, False) and i != king_x and j != king_y:
                                    return False
                        elif king_x > checking_pieces[0][0]:
                            for pos in range(checking_pieces[0][0]+1, king_x):
                                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour == self.board_contents[king_x][king_y].colour and \
                                        (self.board_contents[pos][king_y] is None or self.board_contents[i][j].colour != self.board_contents[pos][king_y].colour) and \
                                        self.board_contents[i][j].is_move_valid(pos, king_y, self.board_contents[pos][king_y], self.board_contents, False) and i != king_x and j != king_y:
                                    return False
                    # Code to see if king can be saved diagonally
                    if king_x != checking_pieces[0][0] and king_y != checking_pieces[0][1] and abs(king_x - checking_pieces[0][0]) == abs(king_y - checking_pieces[0][1]):
                        if king_x < checking_pieces[0][0] and king_y < checking_pieces[0][1]:
                            for pos_x in range(king_x + 1, checking_pieces[0][0]):
                                for pos_y in range(king_y + 1, checking_pieces[0][1]):
                                    if self.board_contents[i][j] is not None and (
                                            self.board_contents[pos_x][pos_y] is None or
                                            self.board_contents[i][j].colour !=
                                            self.board_contents[pos_x][pos_y].colour) and abs(pos_x - king_x) == abs(pos_y - king_y) and \
                                            self.board_contents[i][j].colour == self.board_contents[king_x][
                                            king_y].colour and i != king_x and j != king_y and \
                                            self.board_contents[i][j].is_move_valid(
                                                pos_x, pos_y,
                                                self.board_contents[pos_x][pos_y],
                                                self.board_contents, False):
                                        return False
                        if king_x < checking_pieces[0][0] and king_y > checking_pieces[0][1]:
                            for pos_x in range(king_x + 1, checking_pieces[0][0]):
                                for pos_y in range(checking_pieces[0][1] + 1, king_y):
                                    if self.board_contents[i][j] is not None and (
                                            self.board_contents[pos_x][pos_y] is None or
                                            self.board_contents[i][j].colour !=
                                            self.board_contents[pos_x][pos_y].colour) and abs(pos_x - king_x) == abs(pos_y - king_y) and \
                                            self.board_contents[i][j].colour == self.board_contents[king_x][
                                            king_y].colour and i != king_x and j != king_y and \
                                            self.board_contents[i][j].is_move_valid(
                                                pos_x, pos_y,
                                                self.board_contents[pos_x][pos_y],
                                                self.board_contents, False):
                                        return False
                        if king_x > checking_pieces[0][0] and king_y < checking_pieces[0][1]:
                            for pos_x in range(checking_pieces[0][0] + 1, king_x):
                                for pos_y in range(king_y + 1, checking_pieces[0][1]):
                                    if self.board_contents[i][j] is not None and (
                                            self.board_contents[pos_x][pos_y] is None or
                                            self.board_contents[i][j].colour !=
                                            self.board_contents[pos_x][pos_y].colour) and abs(pos_x - king_x) == abs(pos_y - king_y) \
                                            and self.board_contents[i][j].colour == self.board_contents[king_x][king_y].colour and i != king_x and j != king_y and \
                                            self.board_contents[i][j].is_move_valid(
                                                pos_x, pos_y,
                                                self.board_contents[pos_x][pos_y],
                                                self.board_contents, False):
                                        return False
                        if king_x > checking_pieces[0][0] and king_y > checking_pieces[0][1]:
                            for pos_x in range(checking_pieces[0][0] + 1, king_x):
                                for pos_y in range(checking_pieces[0][1] + 1, king_y):
                                    if self.board_contents[i][j] is not None and (
                                            self.board_contents[pos_x][pos_y] is None or
                                            self.board_contents[i][j].colour !=
                                            self.board_contents[pos_x][pos_y].colour) and abs(pos_x - king_x) == abs(pos_y - king_y) and \
                                            self.board_contents[i][j].colour == self.board_contents[king_x][
                                            king_y].colour and i != king_x and j != king_y and \
                                            self.board_contents[i][j].is_move_valid(
                                                pos_x, pos_y,
                                                self.board_contents[pos_x][pos_y],
                                                self.board_contents, False):
                                        return False
        for i in range(-1, 2):
            for j in range(-1, 2):
                try:
                    if self.board_contents[king_x + i][king_y + j] is None or (self.board_contents[king_x + i][king_x + j] is not None
                                                                               and self.board_contents[king_x][king_y].colour !=
                                                                               self.board_contents[king_x + i][king_y + j].colour):
                        if self.will_be_out_of_checkmate(self.board_contents[king_x][king_y], king_x + i, king_y + j) and 0 <= king_x + i <= 7 and 0 <= king_y + j <= 7:
                            return False
                except IndexError:
                    continue
        return True

    def in_stalemate(self, current_turn):
        any_unblocked_piece = False
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
                        x, y, self.board_contents[x][y], self.board_contents, False):
                    no_checking_pieces += 1
                    checking_pieces.append([i, j])
                if self.board_contents[i][j] is not None and self.board_contents[i][j].colour == \
                   self.board_contents[x][y].colour and not self.board_contents[i][j].is_blocked and i != x and j != y:
                    any_unblocked_piece = True

        if no_checking_pieces > 0:
            return False
        elif pieces_left == 1 or not any_unblocked_piece:
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
