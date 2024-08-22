import os
import numpy as np
import pandas as pd
from tqdm import tqdm

class Node:
    def __init__(self, map=None, bans1=[], bans2=[], team1=[], team2=[]):
        self.map = map

        self.bans1 = bans1
        self.bans2 = bans2

        self.team1 = team1
        self.team2 = team2

class Engine:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        get_data_dir = os.path.join(parent_dir, 'do_analysis')
        data_dir = os.path.join(get_data_dir, 'output')

        with_wins = pd.read_csv(os.path.join(data_dir, 'with_wins.csv'), index_col=0)
        with_games = pd.read_csv(os.path.join(data_dir, 'with_games.csv'), index_col=0)
        against_wins = pd.read_csv(os.path.join(data_dir, 'against_wins.csv'), index_col=0)
        against_games = pd.read_csv(os.path.join(data_dir, 'against_games.csv'), index_col=0)
        winrates = pd.read_csv(os.path.join(data_dir, 'winrates.csv'), index_col=0)

        with_wins = with_wins.fillna(0)
        with_games = with_games.fillna(0)
        against_wins = against_wins.fillna(0)
        against_games = against_games.fillna(0)
        winrates = winrates.fillna(0)

        winrates['Win Rate'] = (winrates['Wins'] + 1) / (winrates['Games'] + 2)
    
        self.data_dir = data_dir

        self.with_winrates = (with_wins + 1) / (with_games + 2)
        self.against_winrates = (against_wins + 1) / (against_games + 2)

        self.winrates = winrates['Win Rate']

        self.brawlers = winrates.sort_values(by='Win Rate', ascending=False).index.to_numpy()

        if os.path.exists(os.path.join(data_dir, 'first_pick.txt')):
            self.first_pick = open(os.path.join(data_dir, 'first_pick.txt'), 'r').readline()
        else:
            self.first_pick = None
    
    def get_data_dir(self):
        return self.data_dir
    
    def get_with_winrates(self):
        return self.with_winrates

    def get_against_winrates(self):
        return self.against_winrates
    
    def get_brawlers(self):
        return self.brawlers

    def get_first_pick(self):
        return self.first_pick

    def get_coefficients(self):
        if os.path.exists(os.path.join(self.data_dir, 'coefficients.txt')):
            parameters = open(os.path.join(self.data_dir, 'coefficients.txt'), 'r').readlines()
            lambda1 = float(parameters[0])
            lambda2 = float(parameters[1])
            lambda3 = float(parameters[2])
            
            return lambda1, lambda2, lambda3
    
        return 1/3, 1/3, 1/3
    
    def evaluation(self, node):
        if len(node.team1) == 0:
            return -float('inf')

        if len(node.team1) == 3 and len(node.team2) == 3:
            value = 0

            for brawler in node.team1:
                value += self.winrates.loc[brawler]
            
            for brawler in node.team2:
                value += 1 - self.winrates.loc[brawler]

            for brawler1 in node.team1:
                for brawler2 in node.team2:
                    value += self.against_winrates.loc[brawler1, brawler2]
            
            for i in range(len(node.team1)):
                for j in range(i+1, len(node.team1)):
                    value += self.with_winrates.loc[node.team1[i], node.team1[j]]
                    value += 1 - self.with_winrates.loc[node.team2[i], node.team2[j]]
            
            return value / 21
        
        individual_value = 0
        invividual_count = 0
        with_value = 0
        against_value = 0
        with_count = 0
        against_count = 0

        for brawler in node.team1:
            individual_value += self.winrates.loc[brawler]
            invividual_count += 1
        
        for brawler in node.team2:
            individual_value += 1 - self.winrates.loc[brawler]
            invividual_count += 1

        for brawler1 in node.team1:
            for brawler2 in node.team2:
                against_value += self.against_winrates.loc[brawler1, brawler2]
                against_count += 1
        
        if len(node.team1) == 1:
            with_value += self.winrates.loc[node.team1[0]]
            with_count += 1
        else:
            for i in range(len(node.team1)):
                for j in range(i+1, len(node.team1)):
                    with_value += self.with_winrates.loc[node.team1[i], node.team1[j]]
                    with_count += 1
        
        if len(node.team2) == 1:
            with_value += 1 - self.winrates.loc[node.team2[0]]
            with_count += 1
        else:
            for i in range(len(node.team2)):
                for j in range(i+1, len(node.team2)):
                    with_value += (1 - self.with_winrates.loc[node.team2[i], node.team2[j]])
                    with_count += 1

        if against_count == 0:
            against_value = with_value
            against_count = with_count

        return (individual_value / invividual_count + with_value / with_count + against_value / against_count) / 3

    def minimax(self, node, depth, alpha, beta, max_depth):
        if depth == 0 or (len(node.team1) == 3 and len(node.team2) == 3):
            return [], self.evaluation(node)

        brawlers = self.brawlers              

        if depth == max_depth:
            brawlers = tqdm(brawlers)

        num1 = len(node.team1)
        num2 = len(node.team2)

        if (num1 == 0 and num2 == 0) or (num1 == 1 and num2 == 2) or (num1 == 2 and num2 == 2):
            isMaximizer = True
        else:
            isMaximizer = False

        best_pick = None
        main_line = []

        if isMaximizer:
            value = -float('inf')

            for brawler in brawlers:
                if brawler not in node.bans1 and brawler not in node.bans2 and brawler not in node.team1 and brawler not in node.team2:
                    node.team1.append(brawler)
                    next_line, new_value = self.minimax(node, depth-1, alpha, beta, max_depth)
                    node.team1.remove(brawler)

                    if new_value > value:
                        value = new_value
                        best_pick = brawler
                        main_line = [best_pick] + next_line
                        
                    alpha = max(alpha, value)

                    if value >= beta:
                        break 
            
        else:
            value = float('inf')

            for brawler in brawlers:
                if brawler not in node.bans1 and brawler not in node.bans2 and brawler not in node.team1 and brawler not in node.team2:
                    node.team2.append(brawler)
                    next_line, new_value = self.minimax(node, depth-1, alpha, beta, max_depth)
                    node.team2.remove(brawler)

                    if new_value < value:
                        value = new_value
                        best_pick = brawler
                        main_line = [best_pick] + next_line

                    beta = min(beta, value)

                    if value <= alpha:
                        break

        return main_line, value

    def get_main_line(self, node, depth):
        num1 = len(node.team1)
        num2 = len(node.team2)

        if num1 > 3 or num2 > 3 or abs(num1 - num2) > 2:
            return -float('inf')

        line = []

        if num1 > 0:
            line.append(node.team1[0])
        if num2 > 0:
            line.append(node.team2[0])
        if num2 > 1:
            line.append(node.team2[1])
        if num1 > 1:
            line.append(node.team1[1])
        if num1 > 2:
            line.append(node.team1[2])
        if num2 > 2:
            line.append(node.team2[2])

        main_line, value = self.minimax(node, depth, -float('inf'), float('inf'), depth)
            
        return line + main_line, value

    def make_teams(self, line):
        n = len(line)

        team1 = []
        team2 = []

        if n > 0:
            team1.append(line[0])
        if n > 1:
            team2.append(line[1])
        if n > 2:
            team2.append(line[2])
        if n > 3:
            team1.append(line[3])
        if n > 4:
            team1.append(line[4])
        if n > 5:
            team2.append(line[5])

        return team1, team2

    def quick_run(self, node, n):
        if n <= 0:
            return [], -float('inf')
        
        while len(node.team1) + len(node.team2) < 6:
            main_line, value = self.get_main_line(node, n)
            node.team1, node.team2 = self.make_teams(main_line)

        return main_line, value

def main():
    engine = Engine()
    node = Node()

    main_line, value = engine.quick_run(node, 4)

    print(main_line)
    print(value)

if __name__ == '__main__':
    main()