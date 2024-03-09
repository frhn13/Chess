import pygame as pg


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def display(self, screen):
        button_pressed = False
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                button_pressed = True
                self.clicked = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return button_pressed
