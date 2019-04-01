from __future__ import division
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import pickle

# Note that we are ignoring game state = 1 because the bestTrade function is available
x_state_2 = [] # Place armies
x_state_3 = [] # Attack
x_state_4 = [] # Roll as attacker
x_state_5 = [] # Move armies to conquered
x_state_6 = [] # Fortify
x_state_10 = [] # Roll as defender

y_state_2 = []
y_state_3 = []
y_state_4 = []
y_state_5 = []
y_state_6 = []
y_state_10 = []

all_attacks = []
all_fortifying_moves = []
all_battle_won_moves = []
all_rolls_attacker = ['retreat', 1, 2, 3]
all_rolls_defender = [1, 2]

def read_attacks():
  f = open("attacks.txt", "r")
  line = f.readline().strip()
  all_attacks.append("endattack")
  while line:
    all_attacks.append(line)
    line = f.readline().strip()

def load_data():
  f = open("easy_vs_hard.txt", "r")
  line = f.readline().strip()

  currentlyTracking = False # Ignore easy player
  readingCountries = False
  gameState = -1
  mustMove = 0
  countries = []
  attack_defend_state = [] # All zeroes, except attacker and defender
  attacker = None
  defender = None

  while line:
    if line == "Current player: Hard":
      currentlyTracking = True
    if currentlyTracking:
      if "Game state:" in line:
        gameState = get_trailing_number(line)
      elif "Attacker:" in line:
        attacker = get_trailing_country(line)
      elif "Defender:" in line and not defender: # Necessary since accidentally wrote defender dice line with just defender
        defender = get_trailing_country(line)
      elif "Countries:" in line:
        readingCountries = True
      elif "Must move:" in line:
        mustMove = get_trailing_number(line)
      elif "--" in line:
        line = f.readline() # Format "Output: [chosen command]"
        if gameState == 1:
          pass
        elif gameState == 2:
          x_state_2.append(countries)
          observed_class = int(line.split()[-2]) # e.g. 39
          y_state_2.append(observed_class)
        elif gameState == 3:
          x_state_3.append(countries)
          if "endattack" in line:
            attack_phrase = "endattack"
          else:
            attack_phrase = " ".join(line.split()[-2:]) # Format "2 3"
          observed_class = all_attacks.index(attack_phrase)
          y_state_3.append(observed_class)
        elif gameState == 4:
          countries.append(countries[attack_defend_state.index(1)])
          countries.append(countries[attack_defend_state.index(-1)])
          x_state_4.append(countries)
          if "retreat" in line:
            roll_phrase = "retreat"
          else:
            roll_phrase = get_trailing_number(line)
          observed_class = all_rolls_attacker.index(roll_phrase) # 0-3
          y_state_4.append(observed_class)
        elif gameState == 5:
          #### Code for worse encoding of features
          # attackInd = attack_defend_state.index(1)
          # attackAmount = countries[attackInd]
          # countries.append(attackAmount)
          # countries.append(mustMove)
          # x_state_5.append(countries)
          # observed_class = get_trailing_number(line)
          # if observed_class not in all_battle_won_moves:
          #   all_battle_won_moves.append(observed_class)
          # y_state_5.append(observed_class)
          countries.extend(attack_defend_state)
          countries.append(mustMove)
          x_state_5.append(countries)
          observed_class = get_trailing_number(line) # Positive number
          if observed_class not in all_battle_won_moves:
            all_battle_won_moves.append(observed_class)
          y_state_5.append(observed_class)
        elif gameState == 6:
          x_state_6.append(countries)
          if "nomove" in line:
            observed_class = "nomove"
          else:
            observed_class = " ".join(line.split()[-3:]) # Format "41 39 1"
          if observed_class not in all_fortifying_moves:
            all_fortifying_moves.append(observed_class)
          y_state_6.append(observed_class)
        elif gameState == 10:
          countries.append(countries[attack_defend_state.index(1)])
          countries.append(countries[attack_defend_state.index(-1)])
          x_state_10.append(countries)
          roll_phrase = get_trailing_number(line)
          observed_class = all_rolls_defender.index(roll_phrase)
          y_state_10.append(observed_class) # Encoding not so important on this case since basically always roll as much as possible
        currentlyTracking = False  # So we don't hit this case on the 2nd set of "--" after output line
        readingCountries = False
        gameState = -1
        mustMove = 0
        countries = []
        attacker = None
        defender = None
        attack_defend_state = []
      elif readingCountries:
        if "Hard" in line:
          countries.append(get_trailing_number(line))
        else:
          countries.append(-get_trailing_number(line))
        if attacker and attacker in line:
          attack_defend_state.append(1)
        elif defender and defender in line:
          attack_defend_state.append(-1)
        else:
          attack_defend_state.append(0)
    line = f.readline().strip()
  all_battle_won_moves.sort()
  for i in range(len(y_state_5)):
    y_state_5[i] = all_battle_won_moves.index(y_state_5[i])
  for i in range(len(y_state_6)):
    y_state_6[i] = all_fortifying_moves.index(y_state_6[i])

def get_trailing_number(s):
  return int(s.split()[-1])

def get_trailing_country(s):
  return " ".join(s.split()[1:])

def fit_model_state_2():
  x_train, x_test, y_train, y_test = train_test_split(x_state_2, y_state_2, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  pickle.dump(model, open('model2.pkl','wb'))

def fit_model_state_3():
  x_train, x_test, y_train, y_test = train_test_split(x_state_3, y_state_3, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  pickle.dump(model, open('model3.pkl','wb'))

def fit_model_state_4():
  x_train, x_test, y_train, y_test = train_test_split(x_state_4, y_state_4, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  pickle.dump(model, open('model4.pkl','wb'))

def fit_model_state_5():
  x_train, x_test, y_train, y_test = train_test_split(x_state_5, y_state_5, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  pickle.dump(model, open('model5.pkl','wb'))

# def fit_model_and_test_state_5_worse():
#   print all_battle_won_moves
#   x_train, x_test, y_train, y_test = train_test_split(x_state_5, y_state_5, test_size=0.3,random_state=109)
#   model = GaussianNB()
#   model.fit(x_train, y_train)
#   pickle.dump(model, open('model5worse.pkl','wb'))

def fit_model_state_6():
  x_train, x_test, y_train, y_test = train_test_split(x_state_6, y_state_6, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  pickle.dump(model, open('model6.pkl','wb'))

def fit_model_state_10():
  x_train, x_test, y_train, y_test = train_test_split(x_state_10, y_state_10, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  pickle.dump(model, open('model10.pkl','wb'))

if __name__ == "__main__":
  read_attacks()
  load_data()
  fit_model_state_2()
  fit_model_state_3()
  fit_model_state_4()
  fit_model_state_5()
  # fit_model_and_test_state_5_worse()
  fit_model_state_6()
  fit_model_state_10()