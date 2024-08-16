import brawlstats
import os
import sys
import io
import pandas as pd
from dotenv import load_dotenv

original_stdout = sys.stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()
api_token = os.getenv('API_TOKEN')

client = brawlstats.Client(api_token)

battlelogs = client.get_battle_logs('8CCYQG9P')

df = pd.DataFrame({'battleTime': [], 'mode': [], 'map': [], 'isRanked': [], 'result': [], 
                   'Player 1,1': [], 'Player 1,2': [], 'Player 1,3': [], 
                   'Player 2,1': [], 'Player 2,2': [], 'Player 2,3': []})
for battlelog in battlelogs:
    battleTime = battlelog['battleTime']
    event = battlelog['event']
    battle = battlelog['battle']

    mode = event['mode']
    map = event['map']

    isRanked = battle['type']
    result = battle['result']
    teams = battle['teams']

    team1 = []
    team2 = []

    for player in teams[0]:
        team1.append(player['brawler']['name'])
    
    for player in teams[1]:
        team2.append(player['brawler']['name'])

    data = pd.DataFrame({'battleTime': [battleTime], 'mode': [mode], 'map': [map], 
                         'isRanked': [isRanked], 'result': [result], 
                         'Player 1,1': [team1[0]], 'Player 1,2': [team1[1]], 'Player 1,3': [team1[2]], 
                         'Player 2,1': [team2[0]], 'Player 2,2': [team2[1]], 'Player 2,3': [team2[2]]})
    
    df = pd.concat([df, data])

df.to_csv('./output/battlelog.csv', index=False)

print(df)

# def log_battle_logs():
#     try:
#         # Get battle logs for a specific player
#         battlelogs = client.get_battle_logs('8CCYQG9P')

#         # Open a log file and write the logs
#         with open('battle_logs.txt', 'a', encoding='utf-8') as log_file:
#             log_file.write(f"\n--- Log Time: {datetime.now()} ---\n")

#             for battle in battlelogs:
#                 log_file.write(str(battle) + '\n')

#         print(f"Logged battle logs at {datetime.now()}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Run the logging process every 30 minutes
# while True:
#     log_battle_logs()
    
#     # Sleep for 30 minutes (30 * 60 seconds)
#     time.sleep(1800)