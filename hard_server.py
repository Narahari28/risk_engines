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

@app.route('/api',methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    gameState = np.array(data['gameState'])
    prediction = None
    if gameState == 2:
    	prediction = predict_state_2(np.array(data['x_state']))
    elif gameState == 3:
    	prediction = predict_state_3(np.array(data['x_state']))
    elif gameState == 4:
    	prediction = predict_state_4(np.array(data['x_state']))
    elif gameState == 5:
    	prediction = predict_state_5(np.array(data['x_state']))
    elif gameState == 6:
    	prediction = predict_state_6(np.array(data['x_state']))
    elif gameState == 10:
    	prediction = predict_state_10(np.array(data['x_state']))
    return jsonify(prediction)

def predict_state_2(x_state):
	test_likelihoods = model2.predict_proba(x_state)
    row = test_likelihoods[i]
    max_prob = 0
    ans = -1
    for j in range(len(row)):
      val = row[j]
      if(val >= max_prob and x_test[i][j] >= 0): # Better than previous best and is not opponent's country
        max_prob = val
        ans = j + 1
	return ans

def predict_state_3(x_state):
	test_likelihoods = model.predict_proba(x_test)
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
    return ans

def predict_state_4(x_state):
	return 1

def predict_state_5(x_state):
	return 1

def predict_state_6(x_state):
	return 1

def predict_state_10(x_state):
	return 1

if __name__ == '__main__':
    app.run(port=5000, debug=True)