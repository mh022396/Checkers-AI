import pygame
from .board import Board
from .constants import BLACK, WHITE, SQUARE_SIZE, GOLD


class Game:
    def __init__(self, window):
        self._init()
        self.window = window
        self.board = Board()

    def update(self):
        """
        Update window display
        """
        pygame.display.update()
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)

    def _init(self):
        """
        For re-initiating game values
        """
        self.selected = None
        self.turn = BLACK
        self.valid_moves = {}
        self.board = Board()

    def reset(self):
        """
        re-initiating game values
        """
        self._init()

    def select(self, row, col):
        """

        :param row: row position selected by mouse
        :param col: column position selected by mouse
        :return: True or False
        """
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True

        return False

    def move(self, row, col):
        """
        check if row and column is a valid move then update the selected piece

        :param row: row to move to
        :param col: column to move to
        :return: True or False based on if move is valid
        """
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def winner(self):
        """
        Check if win condition met
        :return: COLOR value that won
        """
        return self.board.winner()

    def change_turn(self):
        """
        Alternate turn based on color
        """
        self.valid_moves = []
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def draw_valid_moves(self, moves):
        """
        Draw gold boxes for valid moves of selected piece
        :param moves: dictionary {(row, column), []}
        """
        for move in moves:
            row, col = move
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(128)
            s.fill(GOLD)
            self.window.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def get_board(self):
        return self.board

    def ai_move(self, board):
        """
        Set new board and re-initialize game values
        :param board:
        """
        self.board = board
        self.update()
