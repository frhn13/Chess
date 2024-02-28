import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, piece_type, colour, row, column):
        pg.sprite.Sprite.__init__(self)
        self.piece_type = piece_type
        self.colour = colour
        self.row = row
        self.column = column
        self.has_moved = False
        self.is_alive = True

    def is_move_valid(self, new_row, new_column, new_space, board_contents):
        if not (0 <= new_row <= 7 and 0 <= new_column <= 7):
            return False
        if new_row == self.row and new_column == self.column:
            return False
        if self.piece_type == "Pawn":
            if new_row == self.row + 1 and new_column == self.column:
                return True
            elif new_row == self.row + 1 and (
                    new_column == self.row + 1 or new_column == self.row - 1) and new_space is not None:
                return True
            else:
                return False
        elif self.piece_type == "Knight":
            if abs(new_row - self.row) == 2 and abs(new_column - self.column) == 1:
                return True
            elif abs(new_row - self.row) == 1 and abs(new_column - self.column) == 2:
                return True
            else:
                return False
        elif self.piece_type == "King":
            if abs(new_row - self.row) <= 1 and abs(new_column - self.row) <= 1:
                return True
            else:
                return False
        elif self.piece_type == "Rook":
            if self.column == new_column and self.row != new_row:
                if self.row < new_row:
                    for x in range(self.row+1, new_row):
                        if board_contents[x][self.column] is not None:
                            return False
                elif new_row < self.row:
                    for x in range(new_row+1, self.row):
                        if board_contents[x][self.column] is not None:
                            return False
            elif self.column != new_column and self.row == new_row:
                if self.column < new_column:
                    for y in range(self.column+1, new_column):
                        if board_contents[self.row][y] is not None:
                            return False
                elif new_column < self.column:
                    for y in range(new_column+1, self.column):
                        if board_contents[self.row][y] is not None:
                            return False
            else:
                return False
            return True
        elif self.piece_type == "Bishop":
            if abs(self.row-new_row) == abs(self.column-new_column):
                if self.row < new_row and self.column < new_column:
                    for x in range(self.row+1, new_row):
                        for y in range(self.column+1, new_column):
                            if abs(self.row - x) == abs(self.column - y) and board_contents[x][y] is not None:
                                return False
                elif self.row < new_row and self.column > new_column:
                    for x in range(self.row+1, new_row):
                        for y in range(new_column+1, self.column):
                            print(board_contents[x][y])
                            if abs(self.row - x) == abs(self.column - y) and board_contents[x][y] is not None:
                                return False
                elif self.row > new_row and self.column < new_column:
                    for x in range(new_row+1, self.row):
                        for y in range(self.column+1, new_column):
                            print(board_contents[x][y])
                            if abs(self.row - x) == abs(self.column - y) and board_contents[x][y] is not None:
                                return False
                elif self.row > new_row and self.column > new_column:
                    for x in range(new_row+1, self.row):
                        for y in range(new_column+1, self.column):
                            print(board_contents[x][y])
                            if abs(self.row - x) == abs(self.column - y) and board_contents[x][y] is not None:
                                return False
                else:
                    return False
            else:
                return False
            return True
        elif self.piece_type == "Queen":
            pass
