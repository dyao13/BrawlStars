# Brawl Stars

In Brawl Stars, Ranked is a 3v3 game mode. Players draft from 82 brawlers. First, each team secretly chooses 3 brawlers to ban. These bans are then revealed. The teams then draft in a 1, 2, 2, 1 pattern until each team has chosen 3 brawlers. Note that the bans can overlap and that duplicate brawlers cannot be chosen.

We want to determine the optimal strategy for both teams. First, we log the Ranked games of the top 200 (trophies) players. From there, we determine the win rate of each brawler, the win rate of each brawler-brwaler pair with a team, and the win rate of each brawler-brwaler pair in opposing teams. If a brawler-brawler pair is not represented in the data, we subsitute each brawler's overall winrate. We estimate that the probability of victory is the average of all (15 choose 2) of these brawler-brawler pairs.

Given a set of bans, we search for the main line via the minimax algorithm with alpha-beta pruning. This process is computationally expensive, so we construct look-up tables for the final 2 brawler choices, i.e., the last two layers of the search tree. The banning stage may be viewed as a zero-sum game. A payoff matrix is constructed for all (82 choose 3 + 82 choose 4 + 82 choose 5 + 82 choose 6) possible sets of bans where the payoff is the probability of victory with optimal drafting given those bans.
