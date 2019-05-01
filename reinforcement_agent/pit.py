import Arena
from MCTS import MCTS
from risk.RiskGame import RiskGame, display
from risk.RiskPlayers import *
from risk.pytorch.NNet import NNetWrapper as NNet

import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

g = RiskGame()

arr = [ -2,   1,   1,   1,  -2,   1,   1,  -2,  -1,   4,   1,  -1,  -3,
        -5,   4,  -3,   1,  -4,   2,  -1,   1,   2,  -2,   1,   1,  -3,
         2,   1,  -2,  -1,  -1,  -1,   4,   3,   1,   1,   1,   1,   3,
         1,   1,  -2,  18,  19,   0,   4,   0,   4, 124]

print(g.getNextState(arr, 1, 728))

# # all players
# rp = RandomPlayer(g).play
# # gp = GreedyOthelloPlayer(g).play
# # hp = HumanOthelloPlayer(g).play

# # nnet players
# n1 = NNet(g)
# n1.load_checkpoint('./temp_50eps_shorter_4explore_controlled_new_model_oldsearch','temp.pth.tar')
# args1 = dotdict({'numMCTSSims': 50, 'cpuct':3})
# mcts1 = MCTS(g, n1, args1)
# n1p = lambda x: np.random.choice(g.getActionSize(), p=mcts1.getActionProb(x))


# #n2 = NNet(g)
# #n2.load_checkpoint('/dev/8x50x25/','best.pth.tar')
# #args2 = dotdict({'numMCTSSims': 25, 'cpuct':1.0})
# #mcts2 = MCTS(g, n2, args2)
# #n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

# arena = Arena.Arena(n1p, rp, g, display=display)
# print(arena.playGames(10, verbose=True))
