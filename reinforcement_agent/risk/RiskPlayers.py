import numpy as np


class RandomPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        valid_indices = [i for i, x in enumerate(valids) if x == 1]
        index = np.random.randint(len(valid_indices))
        return valid_indices[index]