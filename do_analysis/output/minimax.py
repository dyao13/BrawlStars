import os
import numpy as np
import pandas as pd

class Node:
    def __init__(self, bans1: [], bans2: [], team1: [], team2:[]):
        self.bans1 = bans1
        self.bans2 =bans2

        self.team1 = team1
        self.team2 = team2

class Engine:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        get_data_dir = os.path.join(parent_dir, 'get_data')
        data_dir = os.path.join(get_data_dir, 'output')

        self.with_winrates = pd.read_csv(os.path.join(data_dir, 'withwinrates.csv'))
        self.against_winrates = pd.read_csv(os.path.join(data_dir, 'againstwinrates.csv'))

        self.node = Node()
        
    def evaluation(self, team1, team2):
        with_winrates = self.with_winrates
        against_winrates = self.against_winrates

        value = 0

        for brawler1 in team1:
            for brawler2 in team2:
                value += against_winrates[(brawler1, brawler2)]
        
        value += with_winrates[(team1[0], team1[1])]
        value += with_winrates[(team1[0], team1[2])]
        value += with_winrates[(team1[1], team1[2])]

        value += with_winrates[(team2[0], team2[1])]
        value += with_winrates[(team2[0], team2[2])]
        value += with_winrates[(team2[1], team2[2])]

        value = value / 15

        return value


    def minimax(self, node, depth, alpha, beta, isMaximizer):
        if depth == 0:
            return self.evaluation(node)

        return value

def main():
    engine = Engine()

    print(engine.with_winrates)
    print(engine.against_winrates)

if __name__ == '__main__':
    main()