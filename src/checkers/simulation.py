from copy import deepcopy


def simulate_move(piece, move, board, skip):
    """
    Edit board by simulating move for a piece
    :param piece: piece to simulate move
    :param move: move to simulate
    :param board: current board we are editing our simulation on
    :param skip: pieces we jump over to be removed
    :return: the new edited board
    """
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)
    return board


def get_all_moves(board, color):
    """
    Get all possible boards generated from all possible moves (only one color pieces)
    :param board: Current board state
    :param color: color of pieces to simulate
    :return: generated boards
    """
    moves = []  # these are boards
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)  # these are 'moves' ()
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    return moves
