from BeautifulSoup import BeautifulSoup
import requests
import re
import json

# url = raw_input('')
year = 2012
f = open('gameIds' + str(year) + '.txt', 'w')
for i in range(270):
	string = "http://scores.espn.go.com/nba/scoreboard?date=" + str(year) + "10" + str("{0:0=2d}".format(i))
	s = requests.get(string)
	data = s.text
	soup = BeautifulSoup(data)

	links = soup.findAll('div', {'class': re.compile(r'.*?\bgameLinks\b.*?')})
	# print links
	
	gameIds = []
	for link in links:
		l = link.contents[0]['href']
		gid = re.compile(r'(.*)\=').sub( '', l )
		f.write(str(gid) + '\n')

	print i

f.close()