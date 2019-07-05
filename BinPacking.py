import pandas as pd
import numpy as np


# this method takes an array of teams as an input and outputs a list of round robin games where each team plays each other twice once at home and once away
def roundRobin(teamNames,numberOfGames):
	games = pd.DataFrame(columns = ['awayTeam', 'homeTeam'])

	for p in range (1,numberOfGames/2+1):
		for c in range(1,len(teamNames)+1):
			k=len(teamNames)	
			while k != c:
				awayTeam = teamNames[c-1]
				homeTeam = teamNames[k-1]
				games = games.append(pd.DataFrame({"awayTeam" : [awayTeam], "homeTeam" : [homeTeam]}))
				k=k-1

	gamesReverse = games[['homeTeam', 'awayTeam']]
	gamesReverse = gamesReverse.rename(columns = {'homeTeam': 'awayTeamTemp' , 'awayTeam' : 'homeTeamTemp'})
	gamesReverse = gamesReverse.rename(columns = {'awayTeamTemp': 'awayTeam' , 'homeTeamTemp' : 'homeTeam'})
	games = games.append(gamesReverse)		

	return games

league = ['Boston','New York','Philly','Toronto','Phoenix','Chicago', 'Miami', 'Atlanta', 'Houston', 'San Antonio', 'Los Angeles', 'Golden State', 'OKC', 'Portland', 'Denver', 'Minnesota' ]


teamEast = ['Boston','New York','Philly','Toronto','Chicago', 'Miami', 'Atlanta','Phoenix']
teamWest = ['Houston', 'San Antonio', 'Los Angeles', 'Golden State', 'OKC', 'Portland', 'Denver', 'Minnesota' ]
teamAtlantic = ['Boston', 'Toronto', 'New York', 'Philly']
teamSouthEast = ['Chicago' , 'Miami', 'Atlanta', 'Indiana', 'Phoenix']
teamPacific = ['Los Angeles', 'Golden State', 'Portland', 'Denver']
teamSouthWest = ['Houston', 'San Antonio', 'OKC', 'Minnesota']

#remember to set these properly. set intraconferenceGames equal to actual intraConference games - interconference games etc....
intradivisionGames = 4
intraconferenceGames = 2
interconferenceGames = 2

#creates a list of all games that need to played, order is yet to be determined
roundRobin(teamAtlantic,intradivisionGames)
roundRobin(teamSouthEast,intradivisionGames)
roundRobin(teamPacific,intradivisionGames)
roundRobin(teamSouthWest,intradivisionGames)

roundRobin(teamEast,intraconferenceGames)
roundRobin(teamWest,intraconferenceGames)

roundRobin(league, interconferenceGames)

dfGames = roundRobin(league, interconferenceGames).append(roundRobin(teamWest,intraconferenceGames)).append(roundRobin(teamEast,intraconferenceGames)).append(roundRobin(teamSouthWest,intradivisionGames)).append(roundRobin(teamPacific,intradivisionGames)).append(roundRobin(teamSouthEast,intradivisionGames)).append(roundRobin(teamAtlantic,intradivisionGames))

dfGames = dfGames.reset_index(drop=True)
dfGames['gid'] = dfGames.index

dfGames.to_csv('games.csv')

# each bin object represents a "bin" which is a day
class bin ():
	def __init__(self,dayNumber):
		self.games = pd.DataFrame(columns = ['gid','awayTeam', 'homeTeam'])
		self.dayNum = dayNumber

	def append (self, game):
		self.games = self.games.append(game)


	def numOfGames (self):
		return len(self.games)

	def ifPlaying (self,team):
		if team.awayTeam in self.games.values:
			return True
		elif team.homeTeam in self.games.values:
			return True
		else :
			return False

	def outputDf(self):
		return self.games

	def __str__(self):
		return('Day ' + str(self.dayNum) + '\n' + self.games.to_string())

schedule = []

#create bins so schedule contains bins of x number of days
for dayid in range(1,400):
	gamesList = bin(dayid)
	schedule.append(gamesList)

# assigns games to day bins while making sure no team plays multiple games on the same day
for gameId in range(1,len(dfGames)-5):
	idx = gameId
	for day in schedule:
		did = day.dayNum
		game = dfGames.iloc[idx]

		if schedule[did].ifPlaying(game):
			pass

		elif schedule[did].numOfGames()>10:
			pass
		else :
			schedule[did].append(game)
			break

# parse bin data into singe df to output to csv
outputCsv = pd.DataFrame(columns =['gid','awayTeam', 'homeTeam'])

for d in range (1,99):
	dayString = 'Day' + str(d)
	dayLine = pd.DataFrame({'gid': 0 ,'Day Number' : dayString}, index = [0])
	outputCsv = outputCsv.append(dayLine)
	outputCsv = outputCsv.append(schedule[d].outputDf())

outputCsv = outputCsv [['Day Number', 'gid', 'awayTeam', 'homeTeam']]
outputCsv.to_csv('Schedule.csv', index = False)






