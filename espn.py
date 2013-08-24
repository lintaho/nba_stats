from BeautifulSoup import BeautifulSoup
import requests
import re
import json
from pymongo import MongoClient

# MongoDB setup
connection = MongoClient('localhost', 27017)
db = connection.local
col = db['2013_box_scores']

# TODO add time/location as well as shot types(fast break, etc.) add gameId

f = open('gameIds.txt', 'r+')
for line in f.readlines():
	print line.strip()
	r = requests.get("http://scores.espn.go.com/nba/boxscore?gameId=" + line.strip())
	data = r.text
	soup = BeautifulSoup(data)

	players = soup.findAll('tr', {'class': re.compile(r".*\bplayer\b.*")})

	for p in soup.findAll('div', {'class': 'game-time-location'})[0]:
		print p.text

	break

	trs = soup.findAll('tr')
	# print soup.findAll('tr', 'team-color-strip')[0].th.text
	# print soup.findAll('tr')[0]

	team1 = None
	team1tots = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0']
	t1players = []
	team2 = None
	team2tots = ['0','0','0','0','0','0','0','0','0','0','0','0','0','0']
	t2players = []
	for tr in trs: 
		if 'class' in tr._getAttrMap():
			if team1 == None:
				if tr['class'] == 'team-color-strip':
					team1 = tr.text
			else:
				if tr['class'] == 'team-color-strip':
					team2 = tr.text

			if team2 == None:
				if 'player' in tr['class']:
					t1players.append(tr.contents)
				if tr['class'] == 'even':
					team1tots = tr.contents
			else:
				if 'player' in tr['class']:
					t2players.append(tr.contents)
				if tr['class'] == 'even':
					team2tots = tr.contents

	t1stats = []
	t2stats = []
	for team in [t1players,t2players]:
		stats = []
		for player in team:
			name = player[1].text
			# print player[2].text
			if "DNP" in player[2].text:
				stats.append({"name":name, "played": player[2].text, "min":'0', "fgm-a":'0-0', "3pm-a": '0-0', "oreb":'0', "dreb":'0', "reb":'0',
				"ast":'0', "stl":'0',"blk":'0',"to":'0',"pf":'0',"pm":'0',"pts":'0'})
				continue
			minutes = player[2].text
			fgma = player[3].text 
			tpma = player[4].text
			oreb = player[5].text
			dreb = player[6].text
			reb = player[7].text
			ast = player[8].text
			stl = player[9].text
			blk = player[10].text
			to = player[11].text
			pf = player[12].text
			pm = player[13].text
			pts = player[14].text
			stats.append({"name":name, "played":"P", "min":minutes, "fgm-a":fgma, "3pm-a": tpma, "oreb":oreb, "dreb":dreb, "reb":reb,
				"ast":ast, "stl":stl,"blk":blk,"to":to,"pf":pf,"pm":pm,"pts":pts})
			if t1stats == []:
				t1stats = stats
			else:
				t2stats = stats

	# print t1stats
	# t1stats = json.dumps(t1stats)
		# break
	for t in range(len(team1tots)):
		if type(team1tots[t]) != str:
			team1tots[t] = team1tots[t].text
	for t in range(len(team2tots)):
		if type(team2tots[t]) != str:
			team2tots[t] = team2tots[t].text
	
	# s = open('stats.txt', 'w')
	# with s as outfile:
	col.insert({"gameId": line.strip(), "team1": {"name":team1,
	    "tfgm-a": team1tots[1], "t3pm-a":team1tots[2], "toreb":team1tots[3], 
		"tdreb":team1tots[4], "treb":team1tots[5], "tast": team1tots[6], "tstl": team1tots[7], "tblk":team1tots[8],
		"tto":team1tots[9], "tpf":team1tots[10], "tpts":team1tots[12], "players":t1stats},
		"team2":{"name":team2,     
		"tfgm-a": team2tots[1], "t3pm-a":team2tots[2], "toreb":team2tots[3], 
		"tdreb":team2tots[4], "treb":team2tots[5], "tast": team2tots[6], "tstl": team2tots[7], "tblk":team2tots[8],
		"tto":team2tots[9], "tpf":team2tots[10], "tpts":team2tots[12],"players":t2stats}})
	# s.close()
	# print box_data_json
	# col.insert(box_data_json)

f.close