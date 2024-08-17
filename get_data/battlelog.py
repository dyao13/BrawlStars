import brawlstats
import os
import sys
import io
import pandas as pd
from dotenv import load_dotenv

def log_battles(tag):
    original_stdout = sys.stdout
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if os.path.exists('./output/battlelog.csv'):
        old_df = pd.read_csv('./output/battlelog.csv')
        old_battleTimes = set(old_df['battleTime'])
    else:
        old_df = pd.DataFrame({'battleTime': [], 'mode': [], 'map': [], 'isRanked': [], 'result': [], 'myBrawler': [], 
                            'Player 1,1': [], 'Player 1,2': [], 'Player 1,3': [], 
                            'Player 2,1': [], 'Player 2,2': [], 'Player 2,3': []})
        old_battleTimes = set(old_df['battleTime'])

    load_dotenv()
    api_token = os.getenv('API_TOKEN')

    client = brawlstats.Client(api_token)

    battlelogs = client.get_battle_logs(tag)

    df = pd.DataFrame({'battleTime': [], 'mode': [], 'map': [], 'isRanked': [], 'result': [], 'myBrawler': [], 
                    'Player 1,1': [], 'Player 1,2': [], 'Player 1,3': [], 
                    'Player 2,1': [], 'Player 2,2': [], 'Player 2,3': []})

    for battlelog in battlelogs:
        battleTime = battlelog['battleTime']

        if battleTime in old_battleTimes:
            continue

        old_battleTimes.add(battleTime)

        event = battlelog['event']
        battle = battlelog['battle']

        mode = event['mode']
        map = event['map']

        isRanked = battle['type']

        if not isRanked == 'soloRanked':
            continue

        result = battle['result']
        teams = battle['teams']

        team1 = []
        team2 = []

        for player in teams[0]:
            team1.append(player['brawler']['name'])

            if player['tag'] == '#' + tag:
                myBrawler = player['brawler']['name']
        
        for player in teams[1]:
            team2.append(player['brawler']['name'])

            if player['tag'] == '#' + tag:
                myBrawler = player['brawler']['name']

        data = pd.DataFrame({'battleTime': [battleTime], 'mode': [mode], 'map': [map],
                            'isRanked': [isRanked], 'result': [result], 'myBrawler': [myBrawler], 
                            'Player 1,1': [team1[0]], 'Player 1,2': [team1[1]], 'Player 1,3': [team1[2]], 
                            'Player 2,1': [team2[0]], 'Player 2,2': [team2[1]], 'Player 2,3': [team2[2]]})
        
        df = pd.concat([df, data])

    df = pd.concat([df, old_df], ignore_index=True)

    return df

def main():
    tag = '8CCYQG9P'
    df = log_battles(tag)
    df.to_csv('./output/battlelog.csv', index=False)

    print(df)

if __name__ == '__main__':
    main()
