import chess
import chess.svg
import random as rnd
import time
import math
from numpy import sign

MAX_TURNS = 200
VERBOSE = False
CONSTANT = math.sqrt(2)
ROLLOUT = 25
BEST_PICK = True
MAX_ITERS = 1000
BIG_NUM = 1000000
TINY_NUM = 0.0000001

PAWN = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
]

KNIGHT = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

BISHOP = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

ROCK = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
]

QUEEN = [
    [-20,-10,-10, -5, -5,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5,  5,  5,  5,  0,-10],
    [ -5,  0,  5,  5,  5,  5,  0, -5],
    [  0,  0,  5,  5,  5,  5,  0, -5],
    [-10,  5,  5,  5,  5,  5,  0,-10],
    [-10,  0,  5,  0,  0,  0,  0,-10],
    [-20,-10,-10, -5, -5,-10,-10,-20]
]

KING = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

KING_END = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

PIECES = {}
PIECES['p'] = 100
PIECES['n'] = 320
PIECES['b'] = 330
PIECES['r'] = 500
PIECES['q'] = 900
PIECES['k'] = 1800

TABLES = {}
TABLES['p'] = PAWN
TABLES['n'] = KNIGHT
TABLES['b'] = BISHOP
TABLES['r'] = ROCK
TABLES['q'] = QUEEN
TABLES['k'] = KING

def normalize(value, maxValue, minValue):
    return (value-minValue) / (maxValue-minValue)

def getPiecePosition(turn, index):
    sqName = chess.SQUARE_NAMES[index]
    yPos = 8 - int(sqName[1])
    xPos = int(ord(sqName[0]) - ord('a'))
    if turn:
        return [xPos, yPos]
    return [xPos, 7 - yPos]

def getBoardEvaluation(board):
    white = 0
    black = 0

    pieces = board.piece_map()
    for i in pieces:
        p = pieces[i].symbol().lower()
        pos = getPiecePosition(pieces[i].symbol().isupper(), i)
        if pieces[i].symbol().isupper():
            if not p == 'k':
                white += PIECES[p]
#             white += TABLES[p][pos[1]][pos[0]]
        else:
            if not p == 'k':
                black += PIECES[p]
#             black += TABLES[p][pos[1]][pos[0]]

    if board.is_check():
        if board.turn:
            black += PIECES['k']
        else:
            white += PIECES['k']

    return [white, black]

def logHeuristic(board, turn):
    white = 0
    black = 0

    values = getBoardEvaluation(board)
    white += values[0]
    black += values[1]

    values = board.result().split("-")
    if len(values) > 1:
        if values[0] == "1":
            white += BIG_NUM
        if values[1] == "1":
            black += BIG_NUM
    if turn:
        return math.log(abs((white + TINY_NUM) / (black + TINY_NUM)))
    return math.log(abs((black + TINY_NUM) / (white + TINY_NUM)))

# def nonlogHeuristic(board, turn):
#     white = 0
#     black = 0
#
#     values = getBoardEvaluation(board)
#     white += values[0]
#     black += values[1]
#
#     values = board.result().split("-")
#     if len(values) > 1:
#         if values[0] == "1":
#             white += BIG_NUM
#         if values[1] == "1":
#             black += BIG_NUM
#     if turn:
#         return white - black
#     return black - white
#
# def simpleHeuristic(board, turn):
#     white = 0
#     black = 0
#
#     values = board.result().split("-")
#     if len(values) > 1:
#         if values[0] == "1":
#             white += BIG_NUM
#         if values[1] == "1":
#             black += BIG_NUM
#     if turn:
#         return white - black
#     return black - white

def simpleHeuristic(board, turn):
    white = 0
    black = 0

    values = board.result().split("-")
    if len(values) > 1:
        if values[0] == "1":
            white += 1
        if values[1] == "1":
            black += 1
    if turn:
        return white - black
    return black - white

HEURISTIC = simpleHeuristic
