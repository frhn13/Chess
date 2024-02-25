import pygame as pg


class Piece(pg.sprite.Sprite):
    def __init__(self, piece_type, colour, row, column):
        pg.sprite.Sprite.__init__(self)
        self.piece_type = piece_type
        self.colour = colour
        self.row = row
        self.column = column
        self.is_alive = True
