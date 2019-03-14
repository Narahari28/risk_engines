import re
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics

x_state_2 = [] # Note that we are ignoring game state = 1 because the bestTrade function is available
x_state_3 = []
x_state_4 = []
x_state_5 = []
x_state_6 = []
x_state_10 = []

y_state_2 = []
y_state_3 = []
y_state_4 = []
y_state_5 = []
y_state_6 = []
y_state_10 = []
all_attacks = []

def read_attacks():
  f = open("attacks.txt", "r")
  line = f.readline().strip()
  all_attacks.append("endattack")
  while line:
    all_attacks.append(line)
    line = f.readline().strip()

def load_data():
  lines = []
  f = open("game_state.txt", "r")
  line = f.readline().strip()

  currentlyTracking = False
  readingCountries = False
  gameState = -1
  countries = []
  attack_defend_state = []
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
          pass
        elif gameState == 5:
          pass
        elif gameState == 6:
          pass
        elif gameState == 10:
          pass
        currentlyTracking = False  # So we don't hit this case on the 2nd set of "--" after output line
        readingCountries = False
        gameState = -1
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

def fit_model_and_test_state_2():
  x_train, x_test, y_train, y_test = train_test_split(x_state_2, y_state_2, test_size=0.3,random_state=109)
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
      if(val >= max_prob and x_test[i][j] >= 0): # Better than previous best and is not opponent's country
        max_prob = val
        ans = j + 1
    y_pred.append(ans)
  print("State 2 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets ~28%, much better than 1/21 (own 21 countries on average)

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
      isValidAttack = attackPhrase == "endattack" or ((x_test[i][int(attackPhrase.split()[0]) - 1] >= 0) and (x_test[i][int(attackPhrase.split()[1]) - 1] <= 0))
      if(val >= max_prob and isValidAttack):
        max_prob = val
        ans = j
    y_pred.append(ans)
  print("State 3 Accuracy:", metrics.accuracy_score(y_test, y_pred)) # Gets ~29.5%, much better than 1/20 (20 valid attacks on average)

def fit_model_and_test_state_4():
  pass

def fit_model_and_test_state_5():
  pass

def fit_model_and_test_state_6():
  pass

def fit_model_and_test_state_10():
  pass

if __name__ == "__main__":
  read_attacks()
  load_data()
  # fit_model_and_test_state_2()
  fit_model_and_test_state_3()
  # fit_model_and_test_state_4()
  # fit_model_and_test_state_5()
  # fit_model_and_test_state_6()
  # fit_model_and_test_state_10()