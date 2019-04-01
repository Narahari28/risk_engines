import requests

url = 'http://localhost:5000/api'
r = requests.post(url,json={'gameState': 2, 'x_state': [0] * 42})
print(r.json())