import requests

url = 'http://localhost:5000/api'
r = requests.post(url,json={'gameState': 2, 'x_state': [0]*42, 'offLimits': [], 'maxArmies': 20})
r2 = requests.post(url,json={'gameState': 3, 'x_state': [8,4,1,17,1,1,5,6,8,-10,-7,-8,-6,1,2,12,1,2,1,7,1,1,-9,-9,1,-7,1,1,2,34,1,1,22,-11,1,30,10,1,1,4,1,1], 'offLimits': ["endattack"]})
r3 = requests.post(url,json={'gameState': 4, 'x_state': [-1,-3,-1,-3,3,-3,-4,-1,-5,1,1,1,-2,-1,-3,-2,-1,-1,1,-1,1,-14,1,29,10,1,-3,-1,-1,-1,-1,-2,-1,-1,1,-1,1,-1,-1,-1,-1,-1,3,-3]})
r4 = requests.post(url,json={'gameState': 5, 'x_state': [-9,-17,1,13,1,-6,-10,1,1,-6,-8,1,-10,1,9,7,1,1,1,2,4,13,3,1,0,-6,1,2,2,1,55,71,42,-13,1,1,-1,-10,1,-7,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]})
r5 = requests.post(url,json={'gameState': 6, 'x_state': [1, 2, -3, -1, -1, -2, -1, -1, -1, 3, 1, 5, 1, 1, -3, 2, 1, -2, -2, -1, -4, -1, -1, -2, -3, 1, 1, 1, 1, -4, 1, 1, -3, 1, 1, 1, 1, 1, 5, 1, 2, 2], 'offLimits': []})
r6 = requests.post(url,json={'gameState': 10, 'x_state': [29, 1, 2, 1, 3, 2, 1, 1, 1, 3, 6, 6, 1, 3, 3, 1, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 5, -4, 2, 6, 1, 1, 1, 2, 1, 3, 3, 3, -4, 2]})
print(r.json())
print(r2.json())
print(r3.json())
print(r4.json())
print(r5.json())
print(r6.json())