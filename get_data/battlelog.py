import brawlstats
import os
import sys
import io
import re
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

def get_rankings():
    load_dotenv()
    api_token = os.getenv('API_TOKEN')

    client = brawlstats.Client(api_token)

    rankings = client.get_rankings(ranking='players', region='global')

    tags = []

    for ranking in rankings:
        tags.append(ranking['tag'][1:])

    return tags

def log_battles(tag):
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, tag + 'battlelog.csv')

    if os.path.exists(file_path):
        old_df = pd.read_csv(file_path)
        old_battleTimes = set(old_df['battleTime'])
    else:
        old_df = pd.DataFrame({'battleTime': [], 'mode': [], 'map': [], 
                               'type': [], 'result': [], 'My Brawler': [], 
                               'Tag 1,1': [], 'Brawler 1,1': [], 
                               'Tag 1,2': [], 'Brawler 1,2': [], 
                               'Tag 1,3': [], 'Brawler 1,3': [], 
                               'Tag 2,1': [], 'Brawler 2,1': [], 
                               'Tag 2,2': [], 'Player 2,2': [], 
                               'Tag 2,3': [], 'Player 2,3': []})
        old_battleTimes = set(old_df['battleTime'])

    load_dotenv()
    api_token = os.getenv('API_TOKEN')

    client = brawlstats.Client(api_token)

    battlelogs = client.get_battle_logs(tag)

    df = pd.DataFrame({'battleTime': [], 'mode': [], 'map': [], 
                        'type': [], 'result': [], 'My Brawler': [], 
                        'Tag 1,1': [], 'Brawler 1,1': [], 
                        'Tag 1,2': [], 'Brawler 1,2': [], 
                        'Tag 1,3': [], 'Brawler 1,3': [], 
                        'Tag 2,1': [], 'Brawler 2,1': [], 
                        'Tag 2,2': [], 'Player 2,2': [], 
                        'Tag 2,3': [], 'Player 2,3': []})

    for battlelog in battlelogs:
        battleTime = battlelog['battleTime']

        if battleTime in old_battleTimes:
            continue

        old_battleTimes.add(battleTime)

        event = battlelog['event']
        battle = battlelog['battle']

        if 'mode' in event.keys():
            mode = event['mode']
        else:
            continue

        game_map = event['map']

        if 'type' in battle.keys():
            isRanked = battle['type']
        else:
            isRanked = None

        if not isRanked == 'soloRanked':
            continue

        result = battle['result']
        teams = battle['teams']

        tags1 = []
        tags2 = []

        team1 = []
        team2 = []

        for player in teams[0]:
            tags1.append(player['tag'])
            team1.append(player['brawler']['name'])

            if player['tag'] == '#' + tag:
                myBrawler = player['brawler']['name']
        
        for player in teams[1]:
            tags2.append(player['tag'])
            team2.append(player['brawler']['name'])

            if player['tag'] == '#' + tag:
                myBrawler = player['brawler']['name']

        data = pd.DataFrame({'battleTime': [battleTime], 'mode': [mode], 'map': [game_map],
                            'type': [isRanked], 'result': [result], 'My Brawler': [myBrawler], 
                            'Tag 1,1': [tags1[0]], 'Brawler 1,1': [team1[0]], 
                            'Tag 1,2': [tags1[1]], 'Brawler 1,2': [team1[1]], 
                            'Tag 1,3': [tags1[2]], 'Brawler 1,3': [team1[2]], 
                            'Tag 2,1': [tags2[0]], 'Brawler 2,1': [team2[0]], 
                            'Tag 2,2': [tags2[1]], 'Player 2,2': [team2[1]], 
                            'Tag 2,3': [tags2[2]], 'Player 2,3': [team2[2]]})
        
        df = pd.concat([df, data])

    df = pd.concat([df, old_df], ignore_index=True)

    return df

def get_unique_battles():
    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'battles.csv')

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame({'battleTime': [], 'mode': [], 'map': [], 
                           'type': [], 'result': [], 'My Brawler': [], 
                           'Tag 1,1': [], 'Brawler 1,1': [], 
                           'Tag 1,2': [], 'Brawler 1,2': [], 
                           'Tag 1,3': [], 'Brawler 1,3': [], 
                           'Tag 2,1': [], 'Brawler 2,1': [], 
                           'Tag 2,2': [], 'Player 2,2': [], 
                           'Tag 2,3': [], 'Player 2,3': []})

    files = []

    pattern = re.compile(r'battlelog\.csv$')

    for file in os.listdir(output_dir):
        if pattern.search(file):
            files.append(os.path.join(output_dir, file))
    
    player1 = df['Tag 1,1']
    player2 = df['Tag 1,2']
    player3 = df['Tag 1,3']
    player4 = df['Tag 2,1']
    player5 = df['Tag 2,2']
    player6 = df['Tag 2,3']

    players = []

    for i in range(len(player1)):
            players.append([player1[i], player2[i], player3[i], player4[i], player5[i], player6[i]])

    old_times = set(df['battleTime'])
    old_players = set(frozenset(x) for x in players)

    for j in tqdm(range(len(files))):
        file = files[j]
        battles = pd.read_csv(file)

        times = battles['battleTime']
        
        player1 = battles['Tag 1,1']
        player2 = battles['Tag 1,2']
        player3 = battles['Tag 1,3']
        player4 = battles['Tag 2,1']
        player5 = battles['Tag 2,2']
        player6 = battles['Tag 2,3']

        players = []

        for i in range(len(player1)):
            players.append(frozenset([player1[i], player2[i], player3[i], player4[i], player5[i], player6[i]]))
        
        for i in range(len(times)):
            if times[i] in old_times and players[i] in old_players:
                continue
        
            df = pd.concat([df, pd.DataFrame([battles.iloc[i]])], ignore_index=True)

            old_times.add(times[i])
            old_players.add(frozenset(players[i]))
    
    return df

def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    output_dir = os.path.join(os.path.dirname(__file__), 'output')
    os.makedirs(output_dir, exist_ok=True)

    tags = []

    tags.append('8CCYQG9P')
    tags.append('Y8PLP8VY')

    t200 = get_rankings()

    for tag in t200:
        tags.append(tag)

    for i in tqdm(range(len(tags))):
        tag = tags[i]
        df = log_battles(tag)

        if len(df.index) > 0:
            file_path = os.path.join(output_dir, tag + 'battlelog.csv')
            df.to_csv(file_path, index=False)

    df = get_unique_battles()
    df.to_csv(os.path.join(output_dir, 'battles.csv'), index=False)

if __name__ == '__main__':
    main()
