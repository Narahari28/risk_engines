from Coach import Coach
from risk.RiskGame import RiskGame as Game
from risk.pytorch.NNet import NNetWrapper as nn
from othello.OthelloGame import OthelloGame as Game2
from othello.pytorch.NNet import NNetWrapper as nn2
from utils import *
import numpy as np

args = dotdict({
    'numIters': 50,
    'numEps': 1,
    'tempThreshold': 250,
    'updateThreshold': 0.55,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 75,
    'arenaCompare': 30,
    'cpuct': 10,

    'checkpoint': './temp_1eps_0.001lr_75sims_shorter_4explore_controlled_new_model_fixedMCTS',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

evalArgs = dotdict({
    'numIters': 50,
    'numEps': 1,
    'tempThreshold': 250,
    'updateThreshold': 0.55,
    'maxlenOfQueue': 200000,
    'numMCTSSims': 75,
    'arenaCompare': 30,
    'cpuct': 10,

    'checkpoint': './temp_1eps_0.001lr_75sims_shorter_4explore_controlled_new_model_fixedMCTS',
    'load_model': False,
    'load_folder_file': ('/dev/models/8x100x50','best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

if __name__=="__main__":
    g = Game()
    nnet = nn(g)

    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])

    c = Coach(g, nnet, args, evalArgs)
    if args.load_model:
        print("Load trainExamples from file")
        c.loadTrainExamples()
    c.learn()
