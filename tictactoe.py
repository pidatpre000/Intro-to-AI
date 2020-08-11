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
    xcount=0
    ocount=0
    if board is initial_state():
        return X
    for x in range(3):
        for y in range(3):
            if board[x][y] is X:
                xcount=xcount+1
            elif board[x][y] is O:
                ocount=ocount+1

    if xcount > ocount:

        return O
    else:
       
        return X

    raise NotImplementedError


def actions(board):
    actions=[]
    for i in range(3):
        for j in range(3):
            if board[j][i]==EMPTY:
                actions.append((j,i))
    return actions
    raise NotImplementedError


def result(board, action):
    result= copy.deepcopy(board)
    if action in actions(result):
        result[action[0]][action[1]]=player(result)
    else:
        raise Exception ("invalid")
    
    return result
    raise NotImplementedError


def winner(board):
    #horizontal winner
    for x in range(3):
        if board[x][0]==board[x][1]==board[x][2]:
            if board[x][0] != EMPTY:
                return board[x][0]
        elif board[0][x]==board[1][x]==board[2][x]:
            if board[0][x] != EMPTY:
                return board[0][x]
    if board[0][0]==board[1][1]==board[2][2]:
        if board[0][0] != EMPTY:
            return board[0][0]
    elif board[0][2]==board[1][1]==board[2][0]:
        if board[0][2] != EMPTY:
            return board[0][2]
     
    return None

    raise NotImplementedError
def fullBoard(board):
    for x in range(3):
        for y in range(3):
            if board[x][y] is EMPTY:
                return False
    return True

def terminal(board):
    if (winner(board) is not None) or ((winner(board) is None) and fullBoard(board)):
        return True
    return False
    raise NotImplementedError
    

def utility(board):
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    player_name = player(board)

    if terminal(board):
        return None

    if player_name==X:
        #max score
        val= -math.inf
        move= (-1,-1)

        for action in actions(board):

            opp_val = minval (result(board, action))
            if opp_val > val :
                val= opp_val
                move = action
        return move

    else:
        val= math.inf
        move = (-1,-1)

        for action in actions(board):
        
            opp_val = maxval (result (board, action))
            if opp_val < val :
                val= opp_val
                move = action
        return move


def maxval(board):

    if terminal(board):
        return utility(board)    

    value= -math.inf
    for action in actions(board):
        value = max (value, minval (result (board,action)))
    return value

def minval (board):

    if terminal(board):
        return utility(board)

    value=math.inf
    for action in actions(board):
        value= min(value, maxval (result (board,action) ))
    return value

    raise NotImplementedError
