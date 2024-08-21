import os
import engine
import pandas as pd
from tqdm import tqdm
from itertools import combinations

def save_bans(brawlers):
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isfile(os.path.join(output_dir, 'bans.txt')):
        with open(os.path.join(output_dir, 'bans.txt'), 'w') as output_file:
            for ban in tqdm(list(combinations(brawlers, 6))):
                output_file.write(f"{ban}\n")
            
            for ban in tqdm(list(combinations(brawlers, 5))):
                output_file.write(f"{ban}\n")
            
            for ban in tqdm(list(combinations(brawlers, 4))):
                output_file.write(f"{ban}\n")
            
            for ban in tqdm(list(combinations(brawlers, 3))):
                output_file.write(f"{ban}\n")

def get_teams(subset):
    if len(subset) <= 0 or len(subset) > 6:
        return []
    
    n = len(subset)
    half = n // 2

    halves = list(combinations(subset, half))
    
    partitions = []

    for team1 in halves:
        team2 = set(subset) - set(team1)

        team1 = list(team1)
        team2 = list(team2)

        if n == 3:
            partitions.append([team1, team2])
        else:
            partitions.append([team2, team1])

    return partitions

def save_table(engine, brawlers, depth):
    table = {}

    for subset in list(combinations((brawlers, depth))):
        for teams in get_teams(subset):
            node = engine.Node()

            node.team1 = teams[0]
            node.team2 = teams[1]

            main_line, value = engine.get_main_line(node, 6)
            table[subset] = (main_line, value)

    df = pd.DataFrame(table)
    df.to_csv('table.csv', index=False)

def save_teams(brawlers, n, file_path):
    with open(os.path.join(file_path, 'teams' + str(n) + '.txt'), 'w') as output_file:
        for subset in tqdm(list(combinations(brawlers, n))):
            output_file.write(f"{list(get_teams(subset))}\n")

def main():
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    obj = engine.Engine()
    brawlers = obj.get_brawlers()

    save_bans(brawlers)

    # for ban in tqdm(bans):
    #     available_brawlers = list(set(brawlers) - set(ban))

    #     if not os.path.isfile(os.path.join(output_dir, str(ban) + 'teams4.txt')):
    #         save_teams(available_brawlers, 4, os.path.join(output_dir, str(ban) + 'teams4.txt'))
    #     if not os.path.isfile(os.path.join(output_dir, str(ban) + 'teams5.txt')):
    #         save_teams(available_brawlers, 5, os.path.join(output_dir, str(ban) + 'teams5.txt'))

if __name__ == '__main__':
    main()