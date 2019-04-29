import random
import numpy as np

'''
Author: Narahari Bharadwaj, Apr 5, 2019.
Adapted from Eric P. Nichols, Feb 8, 2008.
Board class.
Board data:
  players: 1 = player 1, -1 = player 2
  pieces[0-41]: armies in each country
  pieces[42]: attacker ind
  pieces[43]: defender ind
  pieces[44]: attacker roll
  pieces[45]: defender roll
  pieces[46]: number to place
  pieces[47]: game state
'''
class Board():
    default_pieces = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, 0, 0, 1, 2]

    def __init__(self, allMoves, pieces=default_pieces, player=1):
        "Set up initial board configuration."

        self.pieces = pieces
        self.allMoves = allMoves
        self.player = player

    def sumAbsCountries(self):
        sum = 0
        for i in range(42):
            sum += abs(self.pieces[i])
        return sum

    def countZeroes(self):
        cnt = 0
        for i in range(42):
            if(self.pieces[i] == 0):
                cnt += 1
        return cnt

    def executePlace(self, action):
        numToPlace = self.pieces[46]
        countryInd = int(action[0]) - 1
        self.pieces[countryInd] += self.player*1
        if(self.sumAbsCountries() < 80):
            self.player *= -1 # Num to place and state stay same (just for other player)
        elif(self.sumAbsCountries() == 80):
            self.player *= -1
            self.pieces[46] = self.calculateArmies()
        else:
            if(numToPlace > 1):
                self.pieces[46] -= 1; # Player and state stay same
            else:
                self.pieces[46] -= 1;
                self.pieces[47] = 3; # Player stays same, but one fewer to place and now attack

    def executeAttack(self, action):
        if action[0] == 'endattack':
            self.pieces[47] = 6
        else:
            self.pieces[42] = int(action[0]) - 1
            self.pieces[43] = int(action[1]) - 1
            self.pieces[47] = 4

    def executeAttackRoll(self, action):
        if action[0] == 'retreat':
            self.pieces[42] = -1
            self.pieces[43] = -1
            self.pieces[45] = 0
            self.pieces[47] = 3
        else:
            self.pieces[44] = int(action[0])
            self.pieces[47] = 10

    def executeMoveConquered(self, action):
        source = self.pieces[42]
        dest = self.pieces[43]
        self.pieces[source] -= int(action[0])*np.sign(self.pieces[source])
        self.pieces[dest] += int(action[0])*np.sign(self.pieces[source])
        self.pieces[42] = -1
        self.pieces[43] = -1
        self.pieces[47] = 3

    def controlsContinent(self, continent):
        for ind in continent:
            if(self.player * self.pieces[ind] <= 0):
                return False
        return True

    def calculateArmies(self):
        europe = [13, 14, 15, 16, 17, 18, 19]
        asia = [26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
        north_am = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        south_am = [9, 10, 11, 12]
        africa = [20, 21, 22, 23, 24, 25]
        australia = [38, 39, 40, 41]
        armies = 0
        territoriesControlled = 0
        for i in range(42):
            if(self.player*self.pieces[i] > 0):
                territoriesControlled += 1
        armies = territoriesControlled / 3
        if(self.controlsContinent(asia)):
            armies += 7
        if(self.controlsContinent(north_am)):
            armies += 5
        if(self.controlsContinent(europe)):
            armies += 5
        if(self.controlsContinent(africa)):
            armies += 3
        if(self.controlsContinent(south_am)):
            armies += 2
        if(self.controlsContinent(australia)):
            armies += 2
        return armies

    def executeFortify(self, action):
        if action[0] == 'nomove':
            self.player = self.player*-1
            self.pieces[46] = self.calculateArmies()
            self.pieces[47] = 2
        else:
            source = int(action[0]) - 1
            dest = int(action[1]) - 1
            count = int(action[2]) - 1
            self.pieces[source] -= count
            self.pieces[dest] += count
            self.player = self.player*-1
            self.pieces[46] = self.calculateArmies()
            self.pieces[47] = 2
        if(self.pieces[46] == 0): # No armies to place, so can only attack
            self.pieces[47] = 3

    def executeDefendRoll(self, action):
        self.pieces[45] = int(action[0])
        attackerRoll = self.pieces[44]
        defenderRoll = self.pieces[45]
        attackerInd = self.pieces[42]
        defenderInd = self.pieces[43]
        attackerDice = [0]*attackerRoll
        defenderDice = [0]*defenderRoll
        for i in range(attackerRoll):
            attackerDice[i] = random.randint(1, 6)
        for i in range(defenderRoll):
            defenderDice[i] = random.randint(1, 6)
        attackerDice.sort(reverse=True)
        defenderDice.sort(reverse=True)
        if(attackerDice[0] > defenderDice[0]):
            self.pieces[defenderInd] -= np.sign(self.pieces[defenderInd])*1
        else:
            self.pieces[attackerInd] -= np.sign(self.pieces[attackerInd])*1
        if(defenderRoll == 2 and attackerRoll >= 2 and attackerDice[1] > defenderDice[1]):
            self.pieces[defenderInd] -= np.sign(self.pieces[defenderInd])*1
        elif(defenderRoll == 2 and attackerRoll >= 2):
            self.pieces[attackerInd] -= np.sign(self.pieces[attackerInd])*1
        if self.pieces[defenderInd] == 0:
            self.pieces[44] = 0
            self.pieces[45] = 0
            self.pieces[47] = 5
        else:
            self.pieces[44] = 0
            self.pieces[45] = 4
            self.pieces[47] = 4

    def executeMove(self, action):
        action = self.allMoves[action]
        # print("action ", action)
        gameState = self.pieces[47]
        if(gameState == 2):
            return self.executePlace(action.split()[1:])
        if(gameState == 3):
            return self.executeAttack(action.split()[1:])
        if(gameState == 4):
            return self.executeAttackRoll(action.split()[1:])
        if(gameState == 5):
            return self.executeMoveConquered(action.split()[1:])
        if(gameState == 6):
            return self.executeFortify(action.split()[1:])
        if(gameState == 10):
            return self.executeDefendRoll(action.split()[1:])

    def validPlaceMoves(self):
        valids = [0]*len(self.allMoves)
        for i in range(len(valids)):
            command = self.allMoves[i].split()
            if(command[0] != 'placearmies'):
                valids[i] = 0
            else:
                loc = int(command[1]) - 1
                cnt = int(command[2])
                can_only_place_on_new = self.countZeroes() > 0
                # print("pieces ", self.pieces)
                # print(loc, cnt, can_only_place_on_new, self.pieces[loc] == 0, self.pieces[loc]*self.player > 0)
                if can_only_place_on_new and self.pieces[loc] == 0 and cnt <= self.pieces[46]:
                    valids[i] = 1
                elif (not can_only_place_on_new) and self.pieces[loc]*self.player > 0 and cnt <= self.pieces[46]:
                    valids[i] = 1
                else:
                    valids[i] = 0
        return np.array(valids)

    def validAttackMoves(self):
        valids = [0]*len(self.allMoves)
        for i in range(len(valids)):
            command = self.allMoves[i].split()
            if(command[0] != 'attack'):
                valids[i] = 0
            else:
                if(command[1] == 'endattack'):
                    valids[i] = 1
                else:
                    attackInd = int(command[1]) - 1
                    defendInd = int(command[2]) - 1
                    if(self.pieces[attackInd]*self.player > 1 and self.pieces[defendInd]*self.player < 0):
                        valids[i] = 1
                    else:
                        valids[i] = 0
        return np.array(valids)

    def validAttackRollMoves(self):
        valids = [0]*len(self.allMoves)
        for i in range(len(valids)):
            command = self.allMoves[i].split()
            if(command[0] != 'attackroll'):
                valids[i] = 0
            else:
                if(command[1] == 'retreat'):
                    if(self.pieces[45] == 4):
                        valids[i] = 1
                    else:
                        valids[i] = 0
                else:
                    attackInd = self.pieces[42]
                    numRoll = int(command[1])
                    if(self.pieces[attackInd] > numRoll):
                        valids[i] = 1
                    else:
                        valids[i] = 0
        return np.array(valids)

    def validMoveConqueredMoves(self):
        valids = [0]*len(self.allMoves)
        for i in range(len(valids)):
            command = self.allMoves[i].split()
            if(command[0] != 'moveconquered'):
                valids[i] = 0
            else:
                moveCnt = int(command[1])
                attackInd = self.pieces[42]
                if(self.pieces[attackInd] > moveCnt):
                    valids[i] = 1
                else:
                    valids[i] = 0
        return np.array(valids)

    def validFortifyMoves(self):
        valids = [0]*len(self.allMoves)
        for i in range(len(valids)):
            command = self.allMoves[i].split()
            if(command[0] != 'fortify'):
                valids[i] = 0
            else:
                if(command[1] == 'nomove'):
                    valids[i] = 1
                else:
                    source = int(command[1]) - 1
                    dest = int(command[2]) - 1
                    cnt = int(command[3])
                    if(self.player*self.pieces[source] > 0 and self.player*self.pieces[dest] > 0 and abs(self.pieces[source]) > cnt):
                        valids[i] = 1
                    else:
                        valids[i] = 0
        return np.array(valids)

    def validDefendRollMoves(self):
        valids = [0]*len(self.allMoves)
        for i in range(len(valids)):
            command = self.allMoves[i].split()
            if(command[0] != 'defendroll'):
                valids[i] = 0
            else:
                defendInd = self.pieces[43]
                numRoll = int(command[1])
                if(abs(self.pieces[defendInd]) >= numRoll):
                    valids[i] = 1
                else:
                    valids[i] = 0
        return np.array(valids)

    def getLegalMoves(self):
        gameState = self.pieces[47]
        if(gameState == 2):
            return self.validPlaceMoves()
        if(gameState == 3):
            return self.validAttackMoves()
        if(gameState == 4):
            return self.validAttackRollMoves()
        if(gameState == 5):
            return self.validMoveConqueredMoves()
        if(gameState == 6):
            return self.validFortifyMoves()
        if(gameState == 10):
            return self.validDefendRollMoves()