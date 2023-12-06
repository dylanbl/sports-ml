import pandas as pd
import datetime
import os
from tabulate import tabulate

def calcStatsDiff(away: [], home: []) -> (): 

    for idx, awayStat in enumerate(away): 
        # Skip team name 
        if idx == 0: 
            continue

        homeStat = float(home[idx])
        awayStat = float(awayStat)

        if homeStat > awayStat: 
            home[idx] = round(homeStat - awayStat, 3)
            away[idx] = '*'
        else: 
            away[idx] = round(awayStat - homeStat, 3)
            home[idx] = '*'

    return (away, home)

def dumpGames(games: [], colHeaders: []):
    dirName = 'data/dailyGameStats/' + str(datetime.date.today()) + '/'
    cmd = 'mkdir ' + dirName
    os.system(cmd) 

    for game in games: 
        awayStats  = game['away']
        homeStats  = game['home']

        fileName = dirName + awayStats[0] + '_at_' + homeStats[0]

        with open(fileName, 'w') as fout: 
            outString = pd.DataFrame(list(zip(colHeaders, awayStats, homeStats)))
            outString = tabulate(outString)

            fout.write(outString)
            fout.close()

    return 

def addPpg(stats: []) -> []: 
    games = stats[1]
    pts   = stats[11]
    oppPts = stats[12]

    stats[11] = round(pts / games, 3)
    stats[12] = round(oppPts / games, 3)
        
def main(): 
    teamStats = pd.read_csv('data/cbbRef/teamAdvStats.csv')
    matchups  = pd.read_csv('data/cbbRef/matchups.csv')

    colHeaders = teamStats.columns
    dailyGames = []

    for idx, game in matchups.iterrows(): 
        # Skip column headers 
        if idx == 0: 
            continue

        awayStats = teamStats[teamStats['school_name'] == game['away']]
        homeStats = teamStats[teamStats['school_name'] == game['home']]

        # Skip D2 schools with no stats
        if len(awayStats) == 0 or len(homeStats) == 0: 
            continue

        awayStatsList = awayStats.values.tolist()[0]
        homeStatsList = homeStats.values.tolist()[0]

        awayStats = addPpg(awayStatsList)
        homeStats = addPpg(homeStatsList)

        awayStaticStats = awayStatsList[:12]
        awayDifferentialStats = awayStatsList[12:]

        homeStaticStats = homeStatsList[:12]
        homeDifferentialStats = homeStatsList[12:]

        awayDifferentialStats, homeDifferentialStats = calcStatsDiff(awayDifferentialStats, homeDifferentialStats) 

        awayStats = awayStaticStats + awayDifferentialStats
        homeStats = homeStaticStats + homeDifferentialStats

        game = {
            'away': awayStats,
            'home': homeStats
        }

        dailyGames.append(game)

    dumpGames(dailyGames, colHeaders)

    return 

if __name__ == "__main__": 
    main() 