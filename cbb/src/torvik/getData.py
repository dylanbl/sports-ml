import requests
import pandas as pd
from headers.headers import teamHeaders, gameHeaders 

def downloadRawData(url: str, path: str): 
    resp = requests.get(url)

    with open(path, 'w') as fout: 
        fout.write(str(resp.content))
        fout.close()

def combineDataWithHeaders(source: str, destination: str, headers: list): 
    df = pd.read_csv(source)
    print(df.columns)
    df.columns = headers
    df = df.drop('null', axis=1)
    df.to_csv(destination, index=False)


def getTeamStats(): 
    downloadRawData('https://barttorvik.com/team-tables_each.php?csv=1',
                    'data/team/teamStats.csv')

    combineDataWithHeaders('data/team/teamStats.csv', 'data/team/teamData.csv',
                           teamHeaders)
    
def getGameStats(): 
    downloadRawData('https://barttorvik.com/team-tables_each.php?csv=1',
                    'data/game/gameStats.csv')

    combineDataWithHeaders('data/game/gameStats.csv', 'data/game/gameData.csv',
                           gameHeaders)
    
def main(): 
    getTeamStats()
    getGameStats()
    
if __name__ == "__main__": 
    main()