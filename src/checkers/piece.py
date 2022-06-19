from .constants import SQUARE_SIZE, CROWN
import pygame


class Piece:
    PADDING = 15
    OUTLINE = 2.5

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

        self.x = 0
        self.y = 0
        self.calc_position()

    def calc_position(self):
        """
        Calculate position visually on display
        """
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, window):
        """
        Draw piece visually on pygame display window
        :param window: pygame display window (800x800 pixels)
        """
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, (0,0,0), (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            window.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        """
        Adjust position variables after moving piece
        :param row: new row position
        :param col: new column position
        """
        self.row = row
        self.col = col
        self.calc_position()

    def __repr__(self):
        return str(self.color)
