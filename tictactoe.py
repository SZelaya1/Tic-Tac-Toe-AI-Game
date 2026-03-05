import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    # Returns starting state of the board.
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    # Returns player who has the next turn on a board.
    X_count = 0
    O_count = 0
    for row in board:
        for element in row:
            if element == X:
                X_count += 1
            elif element == O:
                O_count += 1
    if X_count == O_count:
        return X
    else:
        return O


def actions(board):
    # Returns set of all possible actions (i, j) available on the board.
    possible_actions = set()
    for r_index, row in enumerate(board):
        for index, element in enumerate(row):
            if element == EMPTY:
                possible_actions.add((r_index, index))
    return possible_actions


def result(board, action):
    # Returns the board that results from making move (i, j) on the board.
    new_board = []
    for row in board:
        new_board.append(row.copy())
    if action not in actions(board):
        raise Exception("Invalid action")
    for r_index, row in enumerate(board):
        for index, element in enumerate(row):
            if (r_index, index) == action:
                new_board[r_index][index] = player(board)
    return new_board


def winner(board):
    # Returns the winner of the game, if there is one.
    for i in range(3):
        # Row check
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return X
            elif board[i][0] == O:
                return O
        # Column check
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return X
            elif board[0][i] == O:
                return O
    # Diagonal checks
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return X
        elif board[0][0] == O:
            return O
    if board[2][0] == board[1][1] == board[0][2]:
        if board[2][0] == X:
            return X
        elif board[2][0] == O:
            return O
    return None


def terminal(board):
    # Returns True if game is over, False otherwise.
    if winner(board) is not None:
        return True
    for row in board:
        for element in row:
            if element == EMPTY:
                return False
    return True


def utility(board):
    # Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float("-inf")
    for action in actions(board):
        v = max(v, min_value(result(board, action), alpha, beta))
        alpha = max(alpha, v)
        if alpha >= beta:
            break
    return v


def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = float("inf")
    for action in actions(board):
        v = min(v, max_value(result(board, action), alpha, beta))
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v


def minimax(board):
    # Returns the optimal action for the current player on the board.
    if terminal(board):
        return None

    alpha = float("-inf")
    beta = float("inf")
    if player(board) == X:
        best_value = float("-inf")
        best_action = None
        for action in actions(board):
            value = min_value(result(board, action), alpha, beta)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        best_value = float("inf")
        best_action = None
        for action in actions(board):
            value = max_value(result(board, action), alpha, beta)
            if value < best_value:
                best_value = value
                best_action = action
        return best_action
