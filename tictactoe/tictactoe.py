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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = [x for x in board for x in x]
    if None in flat_board:
        if flat_board.count(None) % 2 == 0:
            return O
        else:
            return X
    return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    flat_board = [x for x in board for x in x]
    actions = [(int(x/3), (x%3)) for x,y in enumerate(flat_board) if y is None]
    return actions
    

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x,y = action
    board2 = copy.deepcopy(board)
    cell = board2[x][y]
    if cell is not None:
        raise Exception('move already made')
    board2[x][y] = player(board)
    return board2

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    flat_board = [x for x in board for x in x]
    if flat_board.count(None) > 4:
        return None

    for i in range(len(board)):
        row = board[i]
        col = [x[i] for x in board]
        diag = [board[0][0], board[1][1], board[2][2]]
        count_diag = [board[0][2], board[1][1], board[2][0]]
        if all(v == col[i] for v in col) and col[i] is not None:
            return col[i]
        elif all(v == row[i] for v in row) and row[i] is not None:
            return row[i]
        elif all(v == diag[i] for v in diag) and diag[i] is not None:
            return diag[i]
        elif all(v == count_diag[i] for v in count_diag) and count_diag[i] is not None:
            return count_diag[i]

    return None
      

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    elif not actions(board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == 'X':
        return 1
    elif winner(board) == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        raise Exception('Game finished')
       
    actions_1 = actions(board)
    if len(actions_1) == 1:
        return actions_1[0]
    
    act_scores_1 = [[] for x in actions_1]
    for i in range(len(actions_1)):
        board_2 = result(board, actions_1[i])
        actions_2 = actions(board_2)
        for j in range(len(actions_2)):
            board_3 = result(board_2, actions_2[j])
            act_scores_1[i].append(utility(board_3))
    print(act_scores_1)
    if player(board) == 'X':
        which_act = []
        for lst in act_scores_1:
            which_act.append(min(lst))
        choose = which_act.index(max(which_act))
    elif player(board) == 'O':
        which_act = []
        for lst in act_scores_1:
            which_act.append(max(lst))
        choose = which_act.index(min(which_act))
        
    return actions_1[choose]
        
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        raise Exception('Game finished')
       
    actions_1 = actions(board)
    if len(actions_1) == 1:
        return actions_1[0]
    
    act_scores_1 = [[[] for x in range(len(actions_1)-1)] for x in actions_1]
    for i in range(len(actions_1)):
        board_2 = result(board, actions_1[i])
        actions_2 = actions(board_2)
        print(actions_2)
        for j in range(len(actions_2)):
            board_3 = result(board_2, actions_2[j])
            actions_3 = actions(board_3)
            print(actions_3)
            for k in range(len(actions_3)):
                board_4 = result(board_3, actions_3[k])
                act_scores_1[i][j].append(utility(board_4))
    print(act_scores_1)
    if player(board) == 'X':
        which_act = []
        for lst in act_scores_1:
            which_subact = []
            for sublst in lst:
                which_subact.append(max(sublst))
            which_act.append(min(lst))
        choose = which_act.index(max(which_act))
    elif player(board) == 'O':
        which_act = []
        for lst in act_scores_1:
            which_subact = []
            for sublst in lst:
                which_subact.append(min(sublst))
            which_act.append(max(lst))
        choose = which_act.index(min(which_act))
        
    return actions_1[choose]
            

def min_value(board):
    if terminal(board):
        return utility(board)
    v = float('inf')
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v      
    
def max_value(board):
    if terminal(board):
        return utility(board)
    v = float('-inf')
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        act = None
        max_v = float('-inf')
        for action in actions(board):
            v2 = min_value(result(board, action))
            if v2 > max_v:
                max_v = v2
                act = action
        return act
    elif player(board) == O:
        act = None
        min_v = float('inf')
        for action in actions(board):
            v2 = max_value(result(board, action))
            if v2 < min_v:
                min_v = v2
                act = action
        return act
    
