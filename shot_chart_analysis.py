from pymongo import MongoClient
import re
import json
import matplotlib as plt
from pylab import *
import numpy as np

# MongoDB setup
connection = MongoClient('localhost', 27017)
db = connection.local
shots = db['2013_shot_chart']
box = db['2013_box_scores']

x = []
y = []
data = []
#Don't forget, two spaces between the name"
for shot in shots.find({"p":"Matt Bonner"}): #, "qtr":"4", "min":{"$lte": "2"}}):
	xc = int(shot['x'])
	yc = int(shot['y'])
	if xc > 50:
		xc = 100-xc
	if yc > 50:
		yc = 100-yc
	x.append(xc)
	y.append(yc)
	data.append({"x":xc*11+30 , "y":yc*10.5+10, "count":1})

print data


# color =['m','g']

# scatter(y,x, s=100 ,marker='o', c=color)
# show()


heatmap, xedges, yedges = np.histogram2d(x, y, bins=100)
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

plt.clf()
plt.imshow(d, extent=extent)
plt.colorbar()
plt.show()

# 	gamedata = box.find_one({"gameId":shot['gameId']})
# 	print gamedata['team1']['name'] + " vs. " + gamedata['team2']['name']

# for game in box.find({"$or":[{"team1.name":"Dallas Mavericks"}, {"team2.name":"Dallas Mavericks"}]}):
# 	if game['team1']['name'] == 'Dallas Mavericks':
# 		# print game['team1']['tto']
# 	else:
# 		# print game['team2']['tto']