from __future__ import division
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import copy

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

  while line:
    if line == "Current player: Hard":
      currentlyTracking = True
    elif line == "Current player: Easy":
      currentlyTracking = False
      readingCountries = False
      gameState = -1
      mustMove = 0
      countries = []
      attack_defend_state = []
      attacker = None
      defender = None
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
          count = int(line.split()[-1])
          while(count > 0):
            x_state_2.append(copy.deepcopy(countries))
            y_state_2.append(str(country) + ' 1')
            countries[country - 1] += 1
            count -= 1
        elif gameState == 3:
          x_state_3.append(copy.deepcopy(countries))
          #print("3 [" + ', '.join(str(c) for c in countries) + ']')
          if "endattack" in line:
            attack_phrase = "endattack"
          else:
            attack_phrase = " ".join(line.split()[-2:]) # Format "2 3"
          observed_class = all_attacks.index(attack_phrase)
          y_state_3.append(observed_class)
        elif gameState == 4:
          countries.append(countries[attack_defend_state.index(1)])
          countries.append(countries[attack_defend_state.index(-1)])
          x_state_4.append(copy.deepcopy(countries))
          #print("4 [" + ', '.join(str(c) for c in countries) + ']')
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
          x_state_5.append(copy.deepcopy(countries))
          #print("5 [" + ', '.join(str(c) for c in countries) + ']')
          observed_class = get_trailing_number(line) # Positive number
          y_state_5.append(observed_class)
        elif gameState == 6:
          x_state_6.append(copy.deepcopy(countries))
          #print("6 [" + ', '.join(str(c) for c in countries) + ']')
          if "nomove" in line:
            observed_class = "nomove"
          else:
            observed_class = " ".join(line.split()[-3:]) # Format "41 39 1"
          y_state_6.append(observed_class)
        elif gameState == 10:
          countries.append(countries[attack_defend_state.index(1)])
          countries.append(countries[attack_defend_state.index(-1)])
          x_state_10.append(copy.deepcopy(countries))
          # print("10 [" + ', '.join(str(c) for c in countries) + ']')
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

def get_trailing_number(s):
  return int(s.split()[-1])

def get_trailing_country(s):
  return " ".join(s.split()[1:])

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def fit_model_and_test_state_2(type):
  global all_placearmies
  x_train, x_test, y_train, y_test = train_test_split(x_state_2, y_state_2, test_size=0.3,random_state=109)
  all_placearmies = list(set(y_train))
  for i in range(len(y_train)):
    y_train[i] = all_placearmies.index(y_train[i])
  for i in range(len(y_test)):
    y_test[i] = all_placearmies.index(y_test[i]) if y_test[i] in all_placearmies else -1
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    can_only_place_on_new = sum(x == 0 for x in x_test[i]) != 0
    can_only_place_one = sum(abs(x) for x in x_test[i]) <= 80
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      potentialMove = all_placearmies[j]
      country = int(potentialMove.split()[0])
      count = int(potentialMove.split()[1])
      maxPlace = 100 # Say max to place is 100
      val = row[j]
      if((can_only_place_one and count > 1) or (can_only_place_on_new and x_test[i][country - 1] != 0) or x_test[i][country - 1] < 0):
        continue
      if(val >= max_prob and count <= maxPlace): # Better than previous best and is not opponent's country
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 2 Accuracy:", metrics.accuracy_score(y_test, y_pred))
  # When all placearmies grouped together: NB: 20.7%, RF: 53.6% much better than 1/838 (838 observed placearmies in total)
  # When placearmies split up: NB: 35.5%, RF: 87.5%
  # RF (initial phase): 85%, Later phase: 89%. Splitting up these into 2 separate datasets doesn't help.

def fit_model_and_test_state_3(type):
  x_train, x_test, y_train, y_test = train_test_split(x_state_3, y_state_3, test_size=0.3,random_state=109)
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      val = row[j]
      attackPhrase = all_attacks[j]
      isValidAttack = attackPhrase == "endattack" or ((x_test[i][int(attackPhrase.split()[0]) - 1] > 1) and (x_test[i][int(attackPhrase.split()[1]) - 1] < 0))
      if(val >= max_prob and isValidAttack):
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 3 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # NB: 32.1%, RF: 35.2% much better than 1/20 (20 valid attacks on average)

def fit_model_and_test_state_4(type):
  x_train, x_test, y_train, y_test = train_test_split(x_state_4, y_state_4, test_size=0.3,random_state=109)
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      val = row[j]
      rollPhrase = all_rolls_attacker[j]
      countryCount = x_test[i][-2]
      isValidRoll = rollPhrase == 'retreat' or countryCount > rollPhrase
      if(val >= max_prob and isValidRoll):
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 4 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # NB: 67.3%, RF: 96.2% much better than 1/4 (4 options in general)

def fit_model_and_test_state_5(type):
  global all_battle_won_moves
  x_train, x_test, y_train, y_test = train_test_split(x_state_5, y_state_5, test_size=0.3,random_state=109)
  all_battle_won_moves = list(set(y_train))
  for i in range(len(y_train)):
    y_train[i] = all_battle_won_moves.index(y_train[i])
  for i in range(len(y_test)):
    y_test[i] = all_battle_won_moves.index(y_test[i]) if y_test[i] in all_battle_won_moves else -1
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    mustMove = x_test[i][-1]
    max_prob = 0
    ans = -1
    countries, attack_defend_state = split_list(x_test[i][:-1])
    attackInd = attack_defend_state.index(1)
    maxMove = countries[attackInd] - 1
    for j in range(len(row)):
      val = row[j]
      potentialMoveCount = all_battle_won_moves[j]
      isValidMove = potentialMoveCount >= mustMove and potentialMoveCount <= maxMove
      if(val >= max_prob and isValidMove):
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 5 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # NB: 31.7%, RF: 31.9% much better than 1/64 (64 observed options in total)


# def fit_model_and_test_state_5_worse():
#   print all_battle_won_moves
#   x_train, x_test, y_train, y_test = train_test_split(x_state_5, y_state_5, test_size=0.3,random_state=109)
#   model = GaussianNB()
#   model.fit(x_train, y_train)
#   test_likelihoods = model.predict_proba(x_test)
#   y_pred = []
#   for i in range(len(x_test)):
#     row = test_likelihoods[i]
#     print row
#     print x_test[i]
#     mustMove = x_test[i][-1]
#     maxMove = x_test[i][-2]
#     max_prob = 0
#     ans = -1
#     for j in range(len(row)):
#       val = row[j]
#       potentialMoveCount = all_battle_won_moves[j]
#       isValidMove = potentialMoveCount >= mustMove and potentialMoveCount <= maxMove
#       if(val >= max_prob and isValidMove):
#         max_prob = val
#         ans = j
#     print ans, y_test[i]
#     y_pred.append(ans)
#   print("State 5 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets 19%

def fit_model_and_test_state_6(type):
  global all_fortifying_moves
  x_train, x_test, y_train, y_test = train_test_split(x_state_6, y_state_6, test_size=0.3,random_state=109)
  all_fortifying_moves = list(set(y_train))
  for i in range(len(y_train)):
    y_train[i] = all_fortifying_moves.index(y_train[i])
  for i in range(len(y_test)):
    y_test[i] = all_fortifying_moves.index(y_test[i]) if y_test[i] in all_fortifying_moves else -1
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  correct_pair_cnt = 0
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      val = row[j]
      potentialMove = all_fortifying_moves[j]
      if(potentialMove == "nomove"):
        isValidMove = True
      else:
        source = int(potentialMove.split()[0])
        destination = int(potentialMove.split()[1])
        armies = int(potentialMove.split()[2])
        isValidMove = x_test[i][source - 1] > armies and x_test[i][destination - 1] >= 0
      if(val >= max_prob and isValidMove):
        max_prob = val
        ans = j
    actualMove = all_fortifying_moves[y_test[i]]
    suggestedMove = all_fortifying_moves[ans]
    if actualMove == suggestedMove:
      correct_pair_cnt += 1
    y_pred.append(ans)
  print("State 6 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # NB: 17.2%, RF: 25.3% much better than 1/451 (451 observed options in total)
  print("State 6 Destination Source Accuracy:", correct_pair_cnt/len(x_test)) # NB: 17.2%, RF: 25.3% much better than 1/164 (164 possible options in total)

def fit_model_and_test_state_10(type):
  x_train, x_test, y_train, y_test = train_test_split(x_state_10, y_state_10, test_size=0.3,random_state=109)
  model = None
  if(type == "forest"):
    model = RandomForestClassifier(n_estimators=100)
  else:
    model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      val = row[j]
      rollPhrase = all_rolls_defender[j]
      countryCount = x_test[i][-1]
      isValidRoll = countryCount >= rollPhrase
      if(val >= max_prob and isValidRoll):
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 10 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # NB: 100%, RF: 100% much better than 1/2 (2 options in general)

def write_all_moves_to_file():
  f = open("all_moves.txt", "w")
  for val in all_placearmies:
    f.write('placearmies ' + val + '\n')
  for val in all_attacks:
    f.write('attack ' + val + '\n')
  for val in all_rolls_attacker:
    f.write('attackroll ' + str(val) + '\n')
  for val in all_battle_won_moves:
    f.write('moveconquered ' + str(val) + '\n')
  for val in all_fortifying_moves:
    f.write('fortify ' + val + '\n')
  for val in all_rolls_defender:
    f.write('defendroll ' + str(val) + '\n')
  f.close()

if __name__ == "__main__":
  read_attacks()
  load_data()
  fit_model_and_test_state_2("forest")
  fit_model_and_test_state_3("forest")
  fit_model_and_test_state_4("forest")
  fit_model_and_test_state_5("forest")
  fit_model_and_test_state_6("forest")
  fit_model_and_test_state_10("forest")
  write_all_moves_to_file()