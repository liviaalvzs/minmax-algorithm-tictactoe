"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def count_values(board):
    """
    Count the values of the board.
    """
    value_counts = {}
    # 2d board into 1d list
    for row in board:
        for cell in row:
            if cell in value_counts:
                value_counts[cell] += 1
            else:
                value_counts[cell] = 1
    
    return value_counts

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counts = count_values(board)
    
    x_count = counts.get(X, 0)
    o_count = counts.get(O, 0)
    
    return 'X' if x_count <= o_count else 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:  
                possible_actions.add((i, j))  
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # checking if action is valid
    if action not in actions(board):
        raise Exception("Not valid action.")
    
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy

def check_rows(board):
    """
    Checks if any row has the same non-None value.
    """
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    return None

def check_columns(board):
    """
    Checks if any column has the same non-None value.
    """
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    return None

def check_diagonals(board):
    """
    Checks if any diagonal has the same non-None value.
    """
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    return check_rows(board) or check_columns(board) or check_diagonals(board)

def check_all_cells_filled(board):
    """
    Returns true if there is no empty values on the board.
    """
    counts = count_values(board)
    empty_count = counts.get(EMPTY, 0)
    if empty_count == 0:
        return True
    else: 
        False

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winner_value = winner(board)
    if winner_value == X or winner_value == O:
        return True
    elif check_all_cells_filled(board):
        return True
    else:
        return False
        
def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_value = winner(board)
    if winner_value == X: 
        return 1
    elif winner_value == O:
        return -1
    else: 
        return 0

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    
    # loop the set of avaliable actions
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
        
    return v
        
def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    
    # loop the set of avaliable actions
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the board is a terminal board, the minimax function should return none
    if terminal(board):
        return None
    
    # given a state s, the maximaxing player picks action a in Actions(s) that produces the highest value of Min-Value(Results(s,a))
    # for minimizing player, the same but choosing the lowest value
    
    player_value = player(board)
    actions_values = actions(board)
    
    if player_value == X:
        plays = []
        for action in actions_values:
            plays.append([min_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]
    
    if player_value == O:
        plays = []
        for action in actions_values:
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0])[0][1]
    
    
    
    