from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game
from .RiskLogic import Board
import numpy as np

all_moves = []

class RiskGame(Game):
    def getInitBoard(self):
        all_moves = []
        f = open("all_moves.txt", "r")
        line = f.readline().strip()
        while line:
            all_moves.append(line)
            line = f.readline().strip()
        b = Board(allMoves=all_moves, player=1)
        return np.array(b.pieces)

    def getBoardSize(self):
        return (1, 49)

    def getActionSize(self):
        all_moves = []
        f = open("all_moves.txt", "r")
        line = f.readline().strip()
        while line:
            all_moves.append(line)
            line = f.readline().strip()
        return len(all_moves)

    def getNextState(self, board, player, action):
        all_moves = []
        f = open("all_moves.txt", "r")
        line = f.readline().strip()
        while line:
            all_moves.append(line)
            line = f.readline().strip()
        b = Board(allMoves=all_moves, pieces=np.copy(board), player=player)
        b.executeMove(action)
        return (b.pieces, b.player)

    def getValidMoves(self, board, player):
        all_moves = []
        f = open("all_moves.txt", "r")
        line = f.readline().strip()
        while line:
            all_moves.append(line)
            line = f.readline().strip()
        b = Board(allMoves=all_moves, pieces=np.copy(board), player=player)
        return b.getLegalMoves()

    def getGameEnded(self, board, player):
        all_positive = True
        all_negative = True
        if board[48] > 75:
            cnt_positive = 0
            cnt_negative = 0
            for i in range(42):
                if(board[i] > 0):
                    cnt_positive += 1
                elif(board[i] < 0):
                    cnt_negative += 1
            if cnt_positive > cnt_negative:
                return 1
            elif cnt_negative > cnt_positive:
                return -1
            else:
                return 1 if sum(board[0:42]) > 0 else -1
        for i in range(42):
            if(board[i] > 0):
                all_negative = False
            elif board[i] < 0:
                all_positive = False
            else:
                return 0
            if not all_negative and not all_positive:
                return 0
        if all_positive:
            return 1
        else:
            return -1

    def getCanonicalForm(self, board, player):
        ans = [0]*len(board)
        for i in range(42):
            ans[i] = board[i]*player
        for i in range(42, 49):
            ans[i] = board[i]
        return np.array(ans)

    def getSymmetries(self, board, pi):
        return [(board, pi)]

    def stringRepresentation(self, board):
        return ' '.join([str(x) for x in board])

def display(board):
    n = board.shape[0]
    print("game state: " + str(board[47]))
    print("num to place: " + str(board[46]))
    print("attacker ind: " + str(board[42]))
    print("defender ind: " + str(board[43]))
    print("attacker roll: " + str(board[44]))
    print("defender roll: " + str(board[45]))
    print("num turns: " + str(board[48]))
    print("countries ", board[0:42])
