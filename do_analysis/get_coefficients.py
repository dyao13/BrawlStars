import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from scipy.optimize import minimize

output_dir = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(output_dir, exist_ok=True)

df = pd.read_csv(os.path.join(output_dir, 'victors.csv'))
with_wins = pd.read_csv(os.path.join(output_dir, 'with_wins.csv'), index_col=0)
with_games = pd.read_csv(os.path.join(output_dir, 'with_games.csv'), index_col=0)
against_wins = pd.read_csv(os.path.join(output_dir, 'against_wins.csv'), index_col=0)
against_games = pd.read_csv(os.path.join(output_dir, 'against_games.csv'), index_col=0)
winrates = pd.read_csv(os.path.join(output_dir, 'winrates.csv'), index_col=0)

with_wins = with_wins.fillna(0) + 1
with_games = with_games.fillna(0) + 2
against_wins = against_wins.fillna(0) + 1
against_games = against_games.fillna(0) + 2

with_winrates = with_wins.div(with_games)
against_winrates = against_wins.div(against_games)

matchups = {}

for row in tqdm(df.itertuples(index=False)):
    victor = row[2]

    if victor == 0:
        continue

    team1 = row[3:6]
    team2 = row[6:9]

    key = tuple(team1 + team2)

    if key not in matchups:
        matchups[key] = (1, 1)

    if victor == 1:
        matchups[key] = (matchups[key][0] + 1, matchups[key][1])
    else:
        matchups[key] = (matchups[key][0], matchups[key][1] + 1)

old_matchups = matchups.copy()
matchups = {}

for key in old_matchups:
    if old_matchups[key][0] + old_matchups[key][1] > 4:
        matchups[key] = old_matchups[key]

keys = list(matchups.keys())
keys.sort()

regression = pd.DataFrame(index=pd.Index(keys), columns=['Win Rate', 'Individual Win Rate', 'With Win Rate', 'Against Win Rate'])

for key in tqdm(keys):
    regression.loc[key, 'Win Rate'] = matchups[key][0] / (matchups[key][0] + matchups[key][1])
    
    individual_rate = 0
    with_rate = 0
    against_rate = 0

    for i in range(3):
        individual_rate += (winrates.loc[key[i], 'Wins'] + 1) / (winrates.loc[key[i], 'Games'] + 2)
        individual_rate += 1 - (winrates.loc[key[i+3], 'Wins'] + 1) / (winrates.loc[key[i+3], 'Games'] + 2)

    for i in range(3):
        for j in range(i+1, 3):
            with_rate += with_winrates.loc[key[i], key[j]]
            with_rate += 1 - with_winrates.loc[key[i+3], key[j+3]]

    for i in range(3):
        for i in range(3, 6):
            against_rate += against_winrates.loc[key[i], key[j]]
    
    regression.loc[key, 'Individual Win Rate'] = individual_rate / 6
    regression.loc[key, 'With Win Rate'] = with_rate / 6
    regression.loc[key, 'Against Win Rate'] = against_rate / 9

regression['Individual Win Rate'] = regression['Individual Win Rate'].astype('float64')
regression['With Win Rate'] = regression['With Win Rate'].astype('float64')
regression['Against Win Rate'] = regression['Against Win Rate'].astype('float64')
regression['Win Rate'] = regression['Win Rate'].astype('float64')

X = regression[['Individual Win Rate', 'With Win Rate', 'Against Win Rate']].to_numpy()
y = regression['Win Rate'].to_numpy()

def objective(coefficients, X, y):
    predictions = np.dot(X, coefficients)
    mse = np.mean((predictions - y) ** 2)

    return mse

def constraint_sum_to_one(coefficients):
    return np.sum(coefficients) - 1

bounds = [(0, 1) for _ in range(X.shape[1])]

initial_guess = np.ones(X.shape[1]) / X.shape[1]

constraints = {'type': 'eq', 'fun': constraint_sum_to_one}

result = minimize(objective, initial_guess, args=(X, y), bounds=bounds, constraints=constraints)

with open(os.path.join(output_dir, 'coefficients.txt'), 'w') as f:
    f.write('\n'.join(map(str, result.x)))

error = np.mean(np.abs(y - np.dot(X, result.x)))

print("Optimal coefficients:", result.x)
print("Error:", error)