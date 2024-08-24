import os
import scipy
import numpy as np
import pandas as pd
from tqdm import tqdm

import engine

def get_payoff_matrix():
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, 'output')

    matrix = pd.read_csv(os.path.join(data_dir, 'payoff_matrix.csv'))

    return matrix

def main():
    obj = engine.Engine()

if __name__ == '__main__':
    main()