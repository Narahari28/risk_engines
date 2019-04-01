# Import libraries
import np
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
    print(data)
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
    return jsonify(output)

def predict_state_2(x_state):
	return None

def predict_state_3(x_state):
	return None

def predict_state_4(x_state):
	return None

def predict_state_5(x_state):
	return None

def predict_state_6(x_state):
	return None

def predict_state_10(x_state):
	return None

if __name__ == '__main__':
    app.run(port=5000, debug=True)