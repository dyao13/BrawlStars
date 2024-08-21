import os
import engine
import ast
import numpy as np
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
            for teams in get_teams(subset):
                output_file.write(f"{teams}\n")

def main():
    current_dir = os.path.dirname(__file__)
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    # obj = engine.Engine()
    # brawlers = obj.get_brawlers()

    # save_bans(brawlers)

    # if not os.path.isfile(os.path.join(output_dir, 'teams4.txt')):
    #     save_teams(available_brawlers, 4, os.path.join(output_dir, 'teams4.txt'))
    # if not os.path.isfile(os.path.join(output_dir, 'teams5.txt')):
    #     save_teams(available_brawlers, 5, os.path.join(output_dir, 'teams5.txt'))

    teams = []

    with open(os.path.join(output_dir, 'teams5.txt'), 'r') as input_file:
        for i, line in tqdm(enumerate(input_file)):
            if i > 10:
                break

            data = ast.literal_eval(line.strip())
            teams.append(data)
        
    print(teams)

    # obj = engine.Engine()
    # node = engine.Node()

    # for team in teams:
    #     node.team1 = 
        

if __name__ == '__main__':
    main()