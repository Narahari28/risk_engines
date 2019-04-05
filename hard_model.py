from __future__ import division
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
from sklearn.externals import joblib

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
all_placearmies = []
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
  previousTurnWasPlace = False
  previousPlaceCountry = None

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
          country = int(line.split()[-2])
          if previousTurnWasPlace and previousPlaceCountry == country:
            old_command = y_state_2[len(y_state_2) - 1]
            old_count = int(old_command.split()[-1])
            new_count = int(line.split()[-1])
            total_count = old_count + new_count
            new_command = str(country) + " " + str(total_count)
            y_state_2[len(y_state_2) - 1] = new_command
          else:
            x_state_2.append(countries)
            # print("2 [" + ', '.join(str(c) for c in countries) + ']')
            observed_class = ' '.join((line.split()[-2:])) # e.g. "39 1"
            if observed_class not in all_placearmies:
              all_placearmies.append(observed_class)
            y_state_2.append(observed_class)
            previousPlaceCountry = country
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
          y_state_5.append(observed_class)
        elif gameState == 6:
          x_state_6.append(countries)
          if "nomove" in line:
            observed_class = "nomove"
          else:
            observed_class = " ".join(line.split()[-3:]) # Format "41 39 1"
          y_state_6.append(observed_class)
        elif gameState == 10:
          countries.append(countries[attack_defend_state.index(1)])
          countries.append(countries[attack_defend_state.index(-1)])
          x_state_10.append(countries)
          roll_phrase = get_trailing_number(line)
          observed_class = all_rolls_defender.index(roll_phrase)
          y_state_10.append(observed_class) # Encoding not so important on this case since basically always roll as much as possible
        if gameState == 2:
          previousTurnWasPlace = True
        else:
          previousTurnWasPlace = False
          previousPlaceCountry = None
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

def get_trailing_number(s):
  return int(s.split()[-1])

def get_trailing_country(s):
  return " ".join(s.split()[1:])

def fit_model_state_2(type):
  all_placearmies = list(set(y_state_2))
  for i in range(len(y_state_2)):
    y_state_2[i] = all_placearmies.index(y_state_2[i])
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_state_2, y_state_2)
  joblib.dump(model, 'model2.pkl', compress=0)

def fit_model_state_3(type):
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_state_3, y_state_3)
  joblib.dump(model, 'model3.pkl', compress=0)

def fit_model_state_4(type):
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_state_4, y_state_4)
  joblib.dump(model, 'model4.pkl', compress=0)

def fit_model_state_5(type):
  all_battle_won_moves = list(set(y_state_5))
  for i in range(len(y_state_5)):
    y_state_5[i] = all_battle_won_moves.index(y_state_5[i])
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_state_5, y_state_5)
  joblib.dump(model, 'model5.pkl', compress=0)

# def fit_model_and_test_state_5_worse():
#   print all_battle_won_moves
#   x_train, x_test, y_train, y_test = train_test_split(x_state_5, y_state_5, test_size=0.3,random_state=109)
#   model = GaussianNB()
#   model.fit(x_train, y_train)
#   pickle.dump(model, open('model5worse.pkl','wb'))

def fit_model_state_6(type):
  all_fortifying_moves = list(set(y_state_6))
  for i in range(len(y_state_6)):
    y_state_6[i] = all_fortifying_moves.index(y_state_6[i])
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_state_6, y_state_6)
  joblib.dump(model, 'model6.pkl', compress=0)

def fit_model_state_10(type):
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_state_10, y_state_10)
  joblib.dump(model, 'model10.pkl', compress=0)

if __name__ == "__main__":
  read_attacks()
  load_data()
  fit_model_state_2("forest")
  fit_model_state_3("forest")
  fit_model_state_4("forest")
  fit_model_state_5("forest")
  # fit_model_and_test_state_5_worse()
  fit_model_state_6("forest")
  fit_model_state_10("forest")