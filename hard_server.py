# Import libraries
import numpy as np
from flask import Flask, request, jsonify
import pickle
app = Flask(__name__)
# Load the model
model2 = pickle.load(open('model2.pkl','rb'))
model3 = pickle.load(open('model3.pkl','rb'))
model4 = pickle.load(open('model4.pkl','rb'))
model5 = pickle.load(open('model5.pkl','rb'))
model6 = pickle.load(open('model6.pkl','rb'))
model10 = pickle.load(open('model10.pkl','rb'))

all_attacks = []
all_fortifying_moves = []
all_battle_won_moves = []
all_placearmies = []
all_rolls_attacker = ['retreat', 1, 2, 3]
all_rolls_defender = [1, 2]
y_state_2 = []

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
            if new_command not in all_placearmies:
              all_placearmies.append(new_command)
          else:
            observed_class = ' '.join((line.split()[-2:])) # e.g. "39 1"
            if observed_class not in all_placearmies:
              all_placearmies.append(observed_class)
            y_state_2.append(observed_class)
            previousPlaceCountry = country
        elif gameState == 3:
          pass
        elif gameState == 4:
          pass
        elif gameState == 5:
          pass
        elif gameState == 6:
          if "nomove" in line:
            observed_class = "nomove"
          else:
            observed_class = " ".join(line.split()[-3:]) # Format "41 39 1"
          if observed_class not in all_fortifying_moves:
            all_fortifying_moves.append(observed_class)
        elif gameState == 10:
          pass
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

def get_trailing_number(s):
	return int(s.split()[-1])

def get_trailing_country(s):
	return " ".join(s.split()[1:])

def split_list(a_list):
	half = len(a_list)//2
	return a_list[:half], a_list[half:]

read_attacks()
load_data()

@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    gameState = data['gameState']
    prediction = None
    if gameState == 2:
    	prediction = predict_state_2(data['x_state'], data['offLimits'])
    elif gameState == 3:
    	prediction = predict_state_3(data['x_state'])
    elif gameState == 4:
    	prediction = predict_state_4(data['x_state'])
    elif gameState == 5:
    	prediction = predict_state_5(data['x_state'])
    elif gameState == 6:
    	prediction = predict_state_6(data['x_state'])
    elif gameState == 10:
    	prediction = predict_state_10(data['x_state'])
    return jsonify(prediction)

def predict_state_2(x_state, offLimits):
	test_likelihoods = model2.predict_proba([x_state])
	can_only_place_on_new = sum(x == 0 for x in x_state[:-1]) != 0
	can_only_place_one = sum(abs(x) for x in x_state[:-1]) <= 80
	row = test_likelihoods[0]
	max_prob = 0
	ans = None
	for j in range(len(row)):
		potentialMove = all_placearmies[j]
		country = int(potentialMove.split()[0])
		count = int(potentialMove.split()[1])
		maxPlace = x_state[-1]
		val = row[j]
		if(country == offLimits or (can_only_place_one and count > 1) or (can_only_place_on_new and x_state[country - 1] != 0) or x_state[country - 1] < 0):
			continue
		if(val >= max_prob and count <= maxPlace): # Better than previous best and is not opponent's country
			max_prob = val
			ans = all_placearmies[j]
	if(ans == None):
		validOptions = []
		for i in range(42):
			if((can_only_place_on_new and x_state[i] != 0) or x_state[i] < 0):
				continue
			validOptions.append(str(i + 1) + " 1")
	print validOptions
	return ans

def predict_state_3(x_state):
	test_likelihoods = model3.predict_proba([x_state])
	row = test_likelihoods[0]
	max_prob = 0
	ans = -1
	for j in range(len(row)):
	  val = row[j]
	  attackPhrase = all_attacks[j]
	  isValidAttack = attackPhrase == "endattack" or ((x_state[int(attackPhrase.split()[0]) - 1] > 1) and (x_state[int(attackPhrase.split()[1]) - 1] < 0))
	  if(val >= max_prob and isValidAttack):
	    max_prob = val
	    ans = j
	return all_attacks[ans]

def predict_state_4(x_state):
	test_likelihoods = model4.predict_proba([x_state])
	row = test_likelihoods[0]
	max_prob = 0
	ans = -1
	for j in range(len(row)):
	  val = row[j]
	  rollPhrase = all_rolls_attacker[j]
	  countryCount = x_state[-2]
	  isValidRoll = rollPhrase == 'retreat' or countryCount > rollPhrase
	  if(val >= max_prob and isValidRoll):
	    max_prob = val
	    ans = j
	return all_rolls_attacker[ans]

def predict_state_5(x_state):
	test_likelihoods = model5.predict_proba([x_state])
	row = test_likelihoods[0]
	mustMove = x_state[-1]
	max_prob = 0
	ans = -1
	countries, attack_defend_state = split_list(x_state[:-1])
	attackInd = attack_defend_state.index(1)
	maxMove = countries[attackInd] - 1
	for j in range(len(row)):
	  val = row[j]
	  potentialMoveCount = all_battle_won_moves[j]
	  isValidMove = potentialMoveCount >= mustMove and potentialMoveCount <= maxMove
	  if(val >= max_prob and isValidMove):
	    max_prob = val
	    ans = all_battle_won_moves[j]
	return ans

def predict_state_6(x_state):
	test_likelihoods = model6.predict_proba([x_state])
	row = test_likelihoods[0]
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
	    isValidMove = x_state[source - 1] > armies and x_state[destination - 1] >= 0
	  if(val >= max_prob and isValidMove):
	    max_prob = val
	    ans = j
	return all_fortifying_moves[ans]

def predict_state_10(x_state):
	test_likelihoods = model10.predict_proba([x_state])
	row = test_likelihoods[0]
	max_prob = 0
	ans = -1
	for j in range(len(row)):
	  val = row[j]
	  rollPhrase = all_rolls_defender[j]
	  countryCount = x_state[-1]
	  isValidRoll = countryCount >= rollPhrase
	  if(val >= max_prob and isValidRoll):
	    max_prob = val
	    ans = j
	return all_rolls_defender[ans]

if __name__ == '__main__':
    app.run(port=5000, debug=True)