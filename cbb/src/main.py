import requests
import pandas as pd
from data.teamHeaders import teamHeaders
from data.gameHeaders import gameHeaders
from classes.Team import Team

def downloadRawData(url: str, path: str): 
    resp = requests.get(url)

    with open(path, 'w') as fout: 
        fout.write(resp.text)
        fout.close()

def combineDataWithHeaders(source: str, destination: str, headers: list): 
    df = pd.read_csv(source)
    df.columns = headers
    df = df.drop('null', axis=1)
    df.to_csv(destination, index=False)


def getTeamStats(): 
    downloadRawData('https://barttorvik.com/team-tables_each.php?csv=1',
                    'data/team/teamStats.csv')

    combineDataWithHeaders('data/team/teamStats.csv', teamHeaders, 
                           'data/team/teamData.csv')
def getGameStats(): 
    downloadRawData('https://barttorvik.com/team-tables_each.php?csv=1',
                    'data/games/gameStats.csv')

    combineDataWithHeaders('data/games/gameStats.csv', gameHeaders, 
                           'data/games/gameData.csv')
    
getGameStats()