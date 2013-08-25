from BeautifulSoup import BeautifulSoup
import requests
import re
import json
from pymongo import MongoClient

# MongoDB setup
connection = MongoClient('localhost', 27017)
db = connection.local
col = db['2013_shot_chart']

f = open('gameIds.txt', 'r+')

for line in f.readlines():
	print line.strip()
	s = requests.get("http://sports.espn.go.com/nba/gamepackage/data/shot?gameId=" + line.strip())
	data = s.text
	soup = BeautifulSoup(data)
	# print soup.contents[0].contents[3]['x']
	shots = []
	for shot in soup.contents[0].contents[1:]:

		x = shot['x']
		sid = shot['id']
		pid = shot['pid']
		qtr = shot['qtr']
		x = shot['x']
		y =  shot['y']
		t = shot['t']
		made = shot['made']
		p = " ".join(shot['p'].split("  "))
		d = shot['d']

		# shots.append(
		col.insert({"gameId":line.strip(),
			"x": x,
			"sid": sid,
			"pid": pid,
			"qtr": qtr,
			"x": x,
			"y": y,
			"t": t,
			"made": made,
			"p": p,
			"d": d})
	# col.insert({"gameID":line.strip(), "shots":shots})
f.close()