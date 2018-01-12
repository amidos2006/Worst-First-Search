import time
import math

MAX_TURNS = 200
VERBOSE = False
CONSTANT = math.sqrt(2)
ROLLOUT = 25
BEST_PICK = True
MAX_ITERS = 1000
BIG_NUM = 1000000
TINY_NUM = 0.0000001

# def getBoardEvaluation(board):
#     white = 0
#     black = 0
#
#     pieces = board.piece_map()
#     for i in pieces:
#         p = pieces[i].symbol().lower()
#         pos = getPiecePosition(pieces[i].symbol().isupper(), i)
#         if pieces[i].symbol().isupper():
#             if not p == 'k':
#                 white += PIECES[p]
# #             white += TABLES[p][pos[1]][pos[0]]
#         else:
#             if not p == 'k':
#                 black += PIECES[p]
# #             black += TABLES[p][pos[1]][pos[0]]
#
#     if board.is_check():
#         if board.turn:
#             black += PIECES['k']
#         else:
#             white += PIECES['k']
#
#     return [white, black]
#
# def logHeuristic(board, turn):
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
#         return math.log(abs((white + TINY_NUM) / (black + TINY_NUM)))
#     return math.log(abs((black + TINY_NUM) / (white + TINY_NUM)))

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
    black = 0
    white = 0

    values = board.result().split("-")
    if len(values) > 1:
        if values[0] == "1":
            black += 1
        if values[1] == "1":
            white += 1
    if turn:
        return black - white
    return white - black

HEURISTIC = simpleHeuristic
