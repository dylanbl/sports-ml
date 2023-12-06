import re
import requests
import datetime 
import pandas as pd
from bs4 import BeautifulSoup

advStatHeaders = [
    'school_name',
    'g',
    'wins',
    'losses',
    'win_loss_pct',
    'srs',
    'sos',
    'wins_conf',
    'losses_conf',
    'wins_home',
    'losses_home',
    'wins_visitor',
    'losses_visitor',
    'pts',
    'opp_pts',
    'pace',
    'off_rtg',
    'fta_per_fga_pct',
    'fg3a_per_fga_pct',
    'ts_pct',
    'trb_pct',
    'ast_pct',
    'stl_pct',
    'blk_pct',
    'efg_pct',
    'tov_pct',
    'orb_pct',
    'ft_rate'
]

matchupHeaders = [
    'away',
    'home',
    'time'
]

def main(): 
    """
    url = 'https://www.sports-reference.com/cbb/seasons/men/2024-advanced-school-stats.html'
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    rows = soup.find('table', id='adv_school_stats').find('tbody').find_all('tr')
    
    df = pd.DataFrame(columns=advStatHeaders)

    for row in rows: 
        cells = row.find_all('td')

        if len(cells) == 0: 
            continue
        
        stats = []
        for cell in cells: 
            stat = cell['data-stat']

            if stat == 'DUMMY': 
                continue
            
            stats.append(cell.get_text())
            
        df.loc[len(df)] = stats

    df = df.drop(columns=['wins_conf', 'losses_conf'], axis=1)
    df.to_csv('data/cbbRef/teamAdvStats.csv', index=False)
    """

    today = datetime.date.today()
    day = today.day
    month = today.month
    year = today.year
    url = 'https://www.sports-reference.com/cbb/boxscores/index.cgi?month={}&day={}&year={}'.format(month, day, year)

    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    games = soup.find('div', class_='game_summaries').findAll('div', {'class': 'gender-m'})

    df = pd.DataFrame(columns=matchupHeaders)

    for game in games: 
        data = game.find_all('td')
        
        game = []
        for item in data: 
            text = item.get_text(strip=True)

            if len(text) == 0 or text == "Men's": 
                continue

            text = re.sub(r"\((.*?)\)", "", text)
            game.append(text)
        
        df.loc[len(df)] = game
    
    df.to_csv('data/cbbRef/matchups.csv', index=False)
            

if __name__ == "__main__": 
    main()