import math
import numpy as np
EPS = 1e-8

class MCTS():
    """
    This class handles the MCTS tree.
    """

    def __init__(self, game, nnet, args):
        self.game = game
        self.nnet = nnet
        self.args = args
        self.Qsa = {}       # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}       # stores #times edge s,a was visited
        self.Ns = {}        # stores #times board s was visited
        self.Ps = {}        # stores initial policy (returned by neural net)

        self.Es = {}        # stores game.getGameEnded ended for board s
        self.Vs = {}        # stores game.getValidMoves for board s

    def getActionProb(self, canonicalBoard, temp=1):
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.

        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)
        """
        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)

        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.game.getActionSize())]
        if temp==0:
            valids = self.game.getValidMoves(canonicalBoard, 1)
            valid_indices = [i for i, x in enumerate(valids) if x == 1]
            best = -1
            bestA = -1
            for ind in valid_indices:
                if(counts[ind] > best):
                    best = counts[ind]
                    bestA = ind
            probs = [0]*len(counts)
            probs[bestA]=1
            return probs

        counts = [x**(1./temp) for x in counts]
        probs = [x/float(sum(counts)) for x in counts]
        valids = self.game.getValidMoves(canonicalBoard, 1)
        valid_indices = [i for i, x in enumerate(valids) if x == 1]
        ans = [0]*len(probs)
        for i in range(len(valid_indices)):
            index = valid_indices[i]
            ans[index] = probs[index]
        if sum(ans) == 0:
            return [x/float(sum(valids)) for x in valids]
        ans = [x/float(sum(ans)) for x in ans]
        return ans


    def search(self, canonicalBoard):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.

        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propogated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propogated up the search path. The values of Ns, Nsa, Qsa are
        updated.

        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.

        Returns:
            v: the negative of the value of the current canonicalBoard
        """

        arg_stack = [canonicalBoard]
        ans_stack = []
        rev_arg_stack = []
        best_action_stack = []

        while(len(arg_stack) > 0):
            canonicalBoard = arg_stack.pop()
            s = self.game.stringRepresentation(canonicalBoard)
            if s not in self.Es:
                self.Es[s] = self.game.getGameEnded(canonicalBoard, 1)
            if self.Es[s]!=0:
                # terminal node
                ans_stack.append(-self.Es[s])
                rev_arg_stack.append(s)
                continue

            if s not in self.Ps:
                # leaf node
                self.Ps[s], v = self.nnet.predict(canonicalBoard)
                valids = self.game.getValidMoves(canonicalBoard, 1)
                self.Ps[s] = self.Ps[s]*valids      # masking invalid moves
                sum_Ps_s = np.sum(self.Ps[s])
                if sum_Ps_s > 0:
                    self.Ps[s] /= sum_Ps_s    # renormalize
                else:
                    # if all valid moves were masked make all valid moves equally probable
                    
                    # NB! All valid moves may be masked if either your NNet architecture is insufficient or you've get overfitting or something else.
                    # If you have got dozens or hundreds of these messages you should pay attention to your NNet and/or training process.   
                    print("All valid moves were masked, do workaround.")
                    self.Ps[s] = self.Ps[s] + valids
                    self.Ps[s] /= np.sum(self.Ps[s])

                self.Vs[s] = valids
                self.Ns[s] = 0
                ans_stack.append(-v)
                rev_arg_stack.append(s)
                continue

            valids = self.Vs[s]
            cur_best = -float('inf')
            best_act = -1

            # pick the action with the highest upper confidence bound
            for a in range(self.game.getActionSize()):
                if valids[a]:
                    if (s,a) in self.Qsa:
                        u = self.Qsa[(s,a)] + self.args.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                    else:
                        u = self.args.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s] + EPS)     # Q = 0 ?

                    if u > cur_best:
                        cur_best = u
                        best_act = a

            a = best_act
            best_action_stack.append(a)
            rev_arg_stack.append(s)
            next_s, next_player = self.game.getNextState(canonicalBoard, 1, a)
            next_s = self.game.getCanonicalForm(next_s, next_player)

            arg_stack.append(next_s)

        cur_val = ans_stack[0]
        for i in reversed(range(len(rev_arg_stack))):
            s = rev_arg_stack[i]
            if(i != len(rev_arg_stack) - 1):
                a = best_action_stack[i - 1]
                if (s,a) in self.Qsa:
                    self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + cur_val)/(self.Nsa[(s,a)]+1)
                    self.Nsa[(s,a)] += 1

                else:
                    self.Qsa[(s,a)] = cur_val
                    self.Nsa[(s,a)] = 1

                self.Ns[s] += 1
                cur_val *= -1
        return cur_val