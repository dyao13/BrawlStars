import os
import numpy as np
import pandas as pd
from tqdm import tqdm

class Node:
    def __init__(self, bans1=[], bans2=[], team1=[], team2=[]):
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

        with_wins = with_wins.fillna(0)
        with_games = with_games.fillna(0)
        against_wins = against_wins.fillna(0)
        against_games = against_games.fillna(0)

        self.with_winrates = (with_wins + 1) / (with_games + 2)
        self.against_winrates = (against_wins + 1) / (against_games + 2)

        winrates = pd.read_csv(os.path.join(data_dir, 'winrates.csv'))

        winrates = winrates.fillna(0)
        
        winrates['Win Rates'] = (winrates['Wins'] + 1) / (winrates['Games'] + 2)
    
        self.brawlers = winrates.sort_values(by='Win Rates', ascending=False)['Name'].to_numpy()
        
    def get_brawlers(self):
        return self.brawlers
    
    def get_with_winrates(self):
        return self.with_winrates

    def get_against_winrates(self):
        return self.against_winrates
    
    def evaluation(self, node):
        value = 0

        for brawler1 in node.team1:
            for brawler2 in node.team2:
                value += self.against_winrates.loc[brawler1, brawler2]
        
        for i in range(len(node.team1)):
            for j in range(i+1, len(node.team2)):
                value += self.with_winrates.loc[node.team1[i], node.team1[j]]
                value += (1 - self.with_winrates.loc[node.team2[i], node.team2[j]])

        value = value / 15

        return value

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

def main():
    engine = Engine()
    node = Node()

    main_line, value = engine.get_main_line(node, 6)
    print(main_line, value)

if __name__ == '__main__':
    main()