from copy import deepcopy
from checkers.constants import WHITE, BLACK
from checkers import simulation
import random


def monte_carlo_tree_search(board, isRoot_F, color_turn, game, rollout_depth, iterations, max_iterations):
    """
    (Tree traversal -> Node expansion -> Rollout -> Backpropagation)
    Algorithm: Start with passed state (board)
    if it is a leaf node:
        If the value of the node (board) is zero:
            Rollout -> Back propagate
        Else:
            foreach available action, add a new state to tree and pass the set the first child as current node and Rollout -> Back propagate
    Else:
        Set the current node to the child node that maximizes the upper bound confidence interval (see in board class) then repeat check for leaf node
    :param board: current board state
    :param isRoot_F: if this is the original root: True else False
    :param color_turn: Whose turn to start the search
    :param game: game logic
    :param rollout_depth: how far are rollouts are
    :param iterations: current iterations of the search loop
    :param max_iterations: the maximimum number of iterations we want to seach
    :return: Best board from available actions
    """
    if isRoot_F:
        board.add_children(simulation.get_all_moves(board, color_turn))

    current = board

    if iterations == max_iterations:
        for c in current.get_children():
            curr = current.get_best_child(iterations)
            curr.reset_mcts()
        return curr

    while current.get_children_len() > 0:
        current = current.get_best_child(iterations)

    if current.get_visits == 0:
        # Rollout
        current_rollout, color = rollout(current, color_turn, rollout_depth)
        # Back propagation
        curr_p = None
        curr_p = back_propagate(current, curr_p, current_rollout, color, color_turn)
        return monte_carlo_tree_search(curr_p, False, color_turn, game, rollout_depth, iterations + 1, max_iterations)

    else:
        if current.get_children_len() == 0:
            current.add_children(simulation.get_all_moves(current, color_turn))

        current = current.get_best_child(iterations)

        # Rollout
        current_rollout, color = rollout(current, color_turn, rollout_depth)
        # Back propagation
        curr_p = None
        curr_p = back_propagate(current, curr_p, current_rollout, color, color_turn)
        return monte_carlo_tree_search(curr_p, False, color_turn, game, rollout_depth, iterations + 1, max_iterations)


def rollout(current, color_turn, rollout_depth):
    """
    Simulate plays randomly to a set depth
    :param current: node to rollout from
    :param color_turn: what turn it is
    :param rollout_depth: how far to rollout/simulate
    :return: current node for rollout and color the simulation ended on
    """
    color = color_turn
    current_rollout = current
    r_iter = 0
    while not current_rollout.winner() is not None or r_iter < rollout_depth:
        r_iter += 1
        current_rollout = get_random_move(current_rollout, color)
        if color == WHITE:
            color = BLACK
        else:
            color = WHITE
        if r_iter == rollout_depth and color != color_turn:
            r_iter -= 1
    return current_rollout, color


def get_random_move(board, color):
    """
    Get board from random legal move
    :param board: current board
    :param color: turn color
    :return: new board generated from random move
    """
    pieces = board.get_all_pieces_move(color)
    piece = random.choice(pieces)
    valid_moves = board.get_valid_moves(piece)
    move = random.choice(list(valid_moves.keys()))
    skip = valid_moves[move]

    temp_board = deepcopy(board)
    temp_piece = temp_board.get_piece(piece.row, piece.col)
    new_board = simulation.simulate_move(temp_piece, move, temp_board, skip)

    return new_board


def back_propagate(current, curr_p, current_rollout, color, color_turn):
    """
    Back propagate to the root and at each node add a visit and a score (100 if win -100 if loss if no end state: heuristic score)
    :param current: current node
    :param curr_p: future parent node
    :param current_rollout: node we are rolling out from
    :param color: color turn we end on
    :param color_turn: current color turn
    :return: curr_p
    """
    while current is not None:
        if current_rollout.winner is not None:
            if color == color_turn:
                current.add_to_total_score(100)
            else:
                current.add_to_total_score(-100)
        elif current_rollout.winner_exception()[1]:
            if color == color_turn:
                current.add_to_total_score(100)
            else:
                current.add_to_total_score(-100)
        else:
            if color == WHITE:
                current.add_to_total_score(current.white_heuristic_eval_1())
            else:
                current.add_to_total_score(current.black_heuristic_eval_1())

        current.increment_visit()
        curr_p = current
        current = current.get_parent()
    return curr_p
