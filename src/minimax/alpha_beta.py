from checkers.constants import WHITE
from checkers import simulation
import random


def alpha_beta(board, depth, max_player, game, heuristic, max_color, min_color, alpha, beta):
    """
    Create a minimax tree by recursively exploring every legal move till max depth is reached. We pass down our alpha and beta
    values and measure if, depending if we are maximizing or minimizing, if a min or max value already explored in the tree has been
    discovered. If so, we do not further explore that node. Evaluate the leaf nodes using a heuristic
    recurse back up the tree and at each node assign either the maximimum or minimum value of its children till reaching the root.
    The root, which in this use case will always be maximizing, then chooses the move that gives the maximum value and returns that value and a
    new board.
    :param board: current board
    :param depth: max depth to extend the minimax tree
    :param max_player: if we are maximizing
    :param game: object containing game logic and visual updates
    :param heuristic: the heuristic evaluation function to give our leaf nodes
    :param max_color: color to maximize on
    :param min_color: color to minimize on
    :param alpha: alpha value (starting at -inf)
    :param beta: beta value (starting at inf)
    :return: best evaluation score and the new board generated from best move
    """
    r = [0, 1]

    if depth == 0 or board.winner():
        if max_color == WHITE:
            if heuristic == 2:
                return board.white_heuristic_eval_2(), board
            elif heuristic == 1:
                return board.white_heuristic_eval_1(), board
            elif heuristic == 3:
                return board.white_heuristic_eval_3(), board
        else:
            if heuristic == 2:
                return board.black_heuristic_eval_2(), board
            elif heuristic == 1:
                return board.black_heuristic_eval_1(), board
            elif heuristic == 3:
                return board.black_heuristic_eval_3(), board

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in simulation.get_all_moves(board, max_color):
            evaluation = alpha_beta(move, depth - 1, False, game, heuristic, max_color, min_color, alpha, beta)[0]
            alpha = max(alpha, evaluation)
            if maxEval == evaluation and best_move is not None:
                if random.choice(r) == 1:
                    best_move = best_move
            else:
                maxEval = max(maxEval, evaluation)
                if maxEval == evaluation:
                    best_move = move
            if beta <= alpha:
                break

        return maxEval, best_move

    else:
        minEval = float('inf')
        best_move = None
        for move in simulation.get_all_moves(board, min_color):
            evaluation = alpha_beta(move, depth - 1, True, game, heuristic, max_color, min_color, alpha, beta)[0]
            beta = min(beta, evaluation)

            if minEval == evaluation and best_move is not None:
                if random.choice(r) == 0:
                    best_move = best_move
            else:
                minEval = min(minEval, evaluation)
                if minEval == evaluation:
                    best_move = move
            if beta <= alpha:
                break

        return minEval, best_move
