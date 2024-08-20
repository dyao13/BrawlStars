import os
import threading
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

        self.with_winrates = pd.read_csv(os.path.join(data_dir, 'with_winrates.csv'), index_col=0)
        self.against_winrates = pd.read_csv(os.path.join(data_dir, 'against_winrates.csv'), index_col=0)
        self.winrates = pd.read_csv(os.path.join(data_dir, 'winrates.csv'))

        for i in range(len(self.with_winrates)):
            self.against_winrates.iloc[i] = self.against_winrates.iloc[i].fillna(self.winrates.iloc[i, 3])
            self.with_winrates.iloc[i] = self.with_winrates.iloc[i].fillna(self.winrates.iloc[i, 3])
    
        self.brawlers = self.winrates['Name'].to_numpy()
        
    def evaluation(self, node):
        value = 0

        for brawler1 in node.team1:
            for brawler2 in node.team2:
                value += self.against_winrates.loc[brawler1, brawler2]
        
        for i in range(len(node.team1)):
            for j in range(i+1, len(node.team2)):
                value += self.with_winrates.loc[node.team1[i], node.team1[j]]
                value += self.with_winrates.loc[node.team2[i], node.team2[j]]

        value = value / 9

        return value

    def minimax(self, node, depth, alpha, beta, isMaximizer, max_depth):
        if depth == 0:
            return [], self.evaluation(node)
        
        if depth == max_depth:
            brawlers = tqdm(self.brawlers)
        else:
            brawlers = self.brawlers

        best_pick = None

        if isMaximizer:
            value = -float('inf')

            for brawler in brawlers:
                if brawler not in node.bans1 and brawler not in node.bans2 and brawler not in node.team1 and brawler not in node.team2:
                    node.team1.append(brawler)
                    
                    next_line, new_value = self.minimax(node, depth-1, alpha, beta, False, max_depth)
                    node.team1.remove(brawler)

                    if new_value > value:
                        value = new_value
                        best_pick = brawler
                        
                    alpha = max(alpha, value)

                    if value > beta:
                        break 
            
        else:
            value = float('inf')

            for brawler in brawlers:
                if brawler not in node.bans1 and brawler not in node.bans2 and brawler not in node.team1 and brawler not in node.team2:
                    node.team2.append(brawler)
                    
                    next_line, new_value = self.minimax(node, depth-1, alpha, beta, True, max_depth)
                    node.team2.remove(brawler)

                    if new_value < value:
                        value = new_value
                        best_pick = brawler

                    beta = min(beta, value)

                    if value < alpha:
                        break

        return [best_pick] + next_line, value

def main():
    engine = Engine()

    engine.node.ban1 = ['PIPER', 'ANGELO', 'MANDY']
    engine.node.ban2 = ['TICK', 'SPROUT', 'GROM']

    engine.node.team1 = ['GENE']

    main_line, value = engine.minimax(engine.node, 5, -float('inf'), float('inf'), False, 5)

    print(main_line, value)

if __name__ == '__main__':
    main()