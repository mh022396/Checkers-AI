import pygame

#display constants
WIDTH = 800
HEIGHT = 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS

#rgb colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (45, 45, 45)
WHITE = (255, 230, 220)
GOLD = (255, 223, 0)
GREY = (128, 128, 128)
#DARK_BEIGE = (225, 198, 153)
DARK_BEIGE = (173, 125, 89)
LIGHT_BEIGE = (237, 212, 173)

CROWN = pygame.transform.scale(pygame.image.load('checkers/assets/crown3.png'), (45, 25))
