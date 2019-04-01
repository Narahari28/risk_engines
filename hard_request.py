import requests

url = 'http://localhost:5000/api'
r = requests.post(url,json={'gameState': 2, 'x_state': [0, 0, 0, 1]})
print(r.json())