from __future__ import division
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

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
  previousPlaceCountry = None;

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
            if new_command not in all_placearmies:
              all_placearmies.append(new_command)
          else:
            countries.append(100) # Say that max to place is 100
            x_state_2.append(countries)
            # print("2 [" + ', '.join(str(c) for c in countries) + ']')
            observed_class = ' '.join((line.split()[-2:])) # e.g. "39 1"
            if observed_class not in all_placearmies:
              all_placearmies.append(observed_class)
            y_state_2.append(observed_class)
            previousPlaceCountry = country
        elif gameState == 3:
          x_state_3.append(countries)
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
          x_state_4.append(countries)
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
          x_state_5.append(countries)
          #print("5 [" + ', '.join(str(c) for c in countries) + ']')
          observed_class = get_trailing_number(line) # Positive number
          y_state_5.append(observed_class)
        elif gameState == 6:
          x_state_6.append(countries)
          #print("6 [" + ', '.join(str(c) for c in countries) + ']')
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
          # print("10 [" + ', '.join(str(c) for c in countries) + ']')
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
  for i in range(110):
    all_battle_won_moves.append(i + 1)
  for i in range(len(y_state_2)):
    y_state_2[i] = all_placearmies.index(y_state_2[i])
  for i in range(len(y_state_5)):
    y_state_5[i] = all_battle_won_moves.index(y_state_5[i])
  for i in range(len(y_state_6)):
    y_state_6[i] = all_fortifying_moves.index(y_state_6[i])

def get_trailing_number(s):
  return int(s.split()[-1])

def get_trailing_country(s):
  return " ".join(s.split()[1:])

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def fit_model_and_test_state_2():
  x_train, x_test, y_train, y_test = train_test_split(x_state_2, y_state_2, test_size=0.3,random_state=109)
  model = GaussianNB()
  model.fit(x_train, y_train)
  test_likelihoods = model.predict_proba(x_test)
  y_pred = []
  for i in range(len(x_test)):
    row = test_likelihoods[i]
    can_only_place_on_new = sum(x == 0 for x in x_test[i][:-1]) != 0
    can_only_place_one = sum(abs(x) for x in x_test[i][:-1]) <= 80
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      potentialMove = all_placearmies[j]
      country = int(potentialMove.split()[0])
      count = int(potentialMove.split()[1])
      maxPlace = x_test[i][-1]
      val = row[j]
      if((can_only_place_one and count > 1) or (can_only_place_on_new and x_test[i][country - 1] != 0) or x_test[i][country - 1] < 0):
        continue
      if(val >= max_prob and count <= maxPlace): # Better than previous best and is not opponent's country
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 2 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets ~13.5%, much better than 1/674 (674 observed placearmies in total)

def fit_model_and_test_state_3():
  x_train, x_test, y_train, y_test = train_test_split(x_state_3, y_state_3, test_size=0.3,random_state=109)
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
  print("State 3 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets ~32.1%, much better than 1/20 (20 valid attacks on average)

def fit_model_and_test_state_4():
  x_train, x_test, y_train, y_test = train_test_split(x_state_4, y_state_4, test_size=0.3,random_state=109)
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
  print("State 4 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets 67.3%, much better than 1/4 (4 options in general)

def fit_model_and_test_state_5():
  x_train, x_test, y_train, y_test = train_test_split(x_state_5, y_state_5, test_size=0.3,random_state=109)
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
  print("State 5 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets 26.5%, much better than 1/74 (74 observed options in total)


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

def fit_model_and_test_state_6():
  x_train, x_test, y_train, y_test = train_test_split(x_state_6, y_state_6, test_size=0.3,random_state=109)
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
    if actualMove == 'nomove' and suggestedMove == 'nomove':
      correct_pair_cnt += 1
    if actualMove != 'nomove' and suggestedMove != 'nomove' and int(suggestedMove.split()[0]) == int(actualMove.split()[0]) and int(suggestedMove.split()[1]) == int(actualMove.split()[1]):
      correct_pair_cnt += 1
    y_pred.append(ans)
  print("State 6 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets 17.3%, much better than 1/530 (530 observed options in total)
  print("State 6 Destination Source Accuracy:", correct_pair_cnt/len(x_test)) # Gets 19.7%, much better than 1/164 (164 possible options in total)

def fit_model_and_test_state_10():
  x_train, x_test, y_train, y_test = train_test_split(x_state_10, y_state_10, test_size=0.3,random_state=109)
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
  print("State 10 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets 100%, much better than 1/2 (2 options in general)

if __name__ == "__main__":
  read_attacks()
  load_data()
  fit_model_and_test_state_2()
  fit_model_and_test_state_3()
  fit_model_and_test_state_4()
  fit_model_and_test_state_5()
  # fit_model_and_test_state_5_worse()
  fit_model_and_test_state_6()
  fit_model_and_test_state_10()