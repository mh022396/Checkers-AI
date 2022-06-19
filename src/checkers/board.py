from .constants import BLACK, ROWS, COLS, SQUARE_SIZE, WHITE, DARK_BEIGE, LIGHT_BEIGE
from .piece import Piece
import pygame
import math
import random


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.black_left = self.white_left = 12
        self.black_kings = 0
        self.white_kings = 0
        self.score = 0
        self.visits = 0
        self.parent = None
        self.parent_action = None
        self.children = []
        self.create_board()

    def reset_mcts(self):
        """
        Reset all variables relevant to Monte Carlo Tree Search
        """
        self.parent = None
        self.score = 0
        self.visits = 0
        self.parent = None
        self.parent_action = None
        self.children = []

    def set_parent(self, board):
        self.parent = board

    def get_parent(self):
        return self.parent

    def increment_visit(self):
        self.visits += 1

    def add_to_total_score(self, score):
        self.score += score

    def add_children(self, children):
        for c in children:
            c.set_parent(self)
        self.children.extend(children)

    def get_children_len(self):
        return self.children.__len__()

    def get_children(self):
        return self.children

    def get_average_score(self):
        return self.score // self.visits

    def get_score(self):
        return self.score

    def get_visits(self):
        return self.visits

    def get_best_child(self, searches):
        """
        Get child with best score. (Monte Carlo Tree Search)
        UCB = (Average_Score) + (2 * sqrt((ln(N) / visits)
        :param searches: N
        :return: Child with best score
        """
        if self.children.__len__() == 0:
            return None
        best = float('-inf')
        best_child = None
        all_zero = True
        for c in self.children:
            all_zero = False
            if c.get_visits() == 0:
                best = float('inf')
                best_child = c
            else:
                ln = math.log(searches)
                ucb = c.get_average_score() + (2 * math.sqrt((ln / c.get_visits())))
                best = max(best, ucb)
                if best > 0:
                    all_zero = False
                if best == ucb:
                    best_child = c
        if all_zero:
            return random.choice(self.children)
        return best_child

    def draw_board(self, window):
        """
        Create the initial 8x8 board visual in the game window
        :param window: pygame display window (800x800 pixels)
        """
        window.fill(DARK_BEIGE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, LIGHT_BEIGE, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def create_board(self):
        """
        Initialize board array (2D) with empty spaces represented by 0 otherwise a new piece
        Adhering to legal starting positions for checkers
        """
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        piece = Piece(row, col, WHITE)
                        self.board[row].append(piece)
                    elif row > 4:
                        piece = Piece(row, col, BLACK)
                        self.board[row].append(piece)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, window):
        """
        Create the initial 8x8 board visual and pieces in the game window
        :param window: pygame display window (800x800 pixels)
        """
        self.draw_board(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    def white_heuristic_eval_1(self):
        """
        Heuristic evaluation focusing on piece count
        :return: Heuristic evaluation
        """
        return self.white_left - self.black_left

    def white_heuristic_eval_2(self):
        """
        Heuristic evaluation focusing on overall piece count and number of kings
        :return: Heuristic evaluation
        """
        return self.white_left - self.black_left + (self.white_kings * .99 - self.black_kings * .99)

    def white_heuristic_eval_3(self):
        """
        Heuristic evaluation focusing on overall piece count, number of kings, and positioning on the board
        :return: Heuristic evaluation
        """
        score = 0
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == WHITE:
                    if not piece.king:
                        if piece.row > 3:
                            score += 2 + piece.row
                        elif piece.row == 0:
                            score += 0
                        else:
                            score += 1 + piece.row
                    else:
                        if self.get_valid_moves(piece).__len__() == 0:
                            score -= 100
                        else:
                            score += 21
                if piece != 0 and piece.color == BLACK:
                    if not piece.king:
                        if piece.row < 4:
                            score -= 3 + (7 - piece.row)
                        else:
                            score -= 2 + (7 - piece.row)
                    else:
                        score -= 21
        return score

    def black_heuristic_eval_1(self):
        """
        Heuristic evaluation focusing on piece count
        :return: Heuristic evaluation
        """
        return self.black_left - self.white_left

    def black_heuristic_eval_2(self):
        """
        Heuristic evaluation focusing on overall piece count and number of kings
        :return: Heuristic evaluation
        """
        return self.black_left - self.white_left + (self.black_kings * .99 - self.white_kings * .99)

    def black_heuristic_eval_3(self):
        """
        Heuristic evaluation focusing on overall piece count, number of kings, and positioning on the board
        :return: Heuristic evaluation
        """
        score = 0
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == BLACK:
                    if not piece.king:
                        if piece.row < 4:
                            score += 2 + (7 - piece.row)

                        else:
                            score += 1 + (7 - piece.row)
                    else:
                        if self.get_valid_moves(piece).__len__() == 0:
                            score -= 100
                        else:
                            score += 21
                if piece != 0 and piece.color == WHITE:
                    if not piece.king:
                        if piece.row > 5:
                            score -= 3 + piece.row
                        else:
                            score -= 2 + piece.row
                    else:
                        score -= 21
        return score

    def get_all_pieces(self, color):
        """
        Find all pieces in the board array of certain color
        :param color: Color of wanted pieces
        :return: All pieces of color
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def get_all_pieces_move(self, color):
        """
        Find all pieces in the board array of certain color and have at least one valid move
        (not blocked)
        :param color: Color of wanted pieces
        :return: All pieces of color and have at least one available move
        """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color and self.get_valid_moves(piece).__len__() > 0:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        """
        Move selected piece within our board array to a new index
        If move results in a king (piece meeting row 0 or ROW and is corresponding color)
        make piece a king and add to our king count
        :param piece: piece to move
        :param row: new row position
        :param col: new column position
        """
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            if piece.color == WHITE and not piece.king:
                self.white_kings += 1
                piece.make_king()
            elif piece.color == BLACK and not piece.king:
                self.black_kings += 1
                piece.make_king()

    def remove(self, pieces):
        """
        Remove piece or pieces from board array and update counts
        :param pieces: piece or pieces to be removed
        """
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLACK:
                    if piece.king:
                        self.black_left -= 1
                        self.black_kings -= 1
                    else:
                        self.black_left -= 1
                else:
                    if piece.king:
                        self.white_left -= 1
                        self.white_kings -= 1
                    else:
                        self.white_left -= 1

    def winner(self):
        """
        Check if win condition met (one color has no pieces left)
        :return:
        """
        if self.black_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return BLACK
        return None

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        """
        Get all possible moves for a piece
        :param piece: piece to search
        :return: available moves for a piece {(row,col) -> []}
        """
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == BLACK or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    if skipped:
                        moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last + skipped))
                        moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last + skipped))
                    else:
                        moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                        moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    if skipped:
                        moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last + skipped))
                        moves.update(
                            self._traverse_right(r + step, row, step, color, right + 1, skipped=last + skipped))
                    else:
                        moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                        moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
