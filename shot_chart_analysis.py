from pymongo import MongoClient
import re
import json

# MongoDB setup
connection = MongoClient('localhost', 27017)
db = connection.local
shots = db['2013_shot_chart']
box = db['2013_box_scores']

#Don't forget, two spaces between the name"
# for shot in shots.find({"p":"Jeremy  Lin", "made":"true", "qtr":"4", "y":{"$gt" : "15"}}):
	# gamedata = box.find_one({"gameId":shot['gameId']})
	# print gamedata['team1']['name'] + " vs. " + gamedata['team2']['name']

for game in box.find({"$or":[{"team1.name":"Dallas Mavericks"}, {"team2.name":"Dallas Mavericks"}]}):
	if game['team1']['name'] == 'Dallas Mavericks':
		print game['team1']['tto']
	else:
		print game['team2']['tto']