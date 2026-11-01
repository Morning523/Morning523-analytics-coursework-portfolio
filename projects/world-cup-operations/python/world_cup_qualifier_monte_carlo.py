"""
Monte Carlo Simulation for 2026 FIFA World Cup Remaining Qualifiers
=====================================================================
Uses actual FIFA Ranking Points (January 2026) as Elo ratings to derive
win probabilities for playoff matches.
Simulates all 6 remaining playoff spots across 10,000 iterations.

Formula: E_A = 1 / (1 + 10^((R_B - R_A) / 600))
Note: FIFA uses a divisor of 600 (not 400 as in classic Elo) for international football.

Data Source: FIFA/Coca-Cola Men's World Ranking, 19 January 2026
Reference: Robberechts & Davis (2018); Groll et al. (2015)

Course: IB9190 Advanced Analytics, University of Warwick
"""

import numpy as np
import pandas as pd
from collections import Counter
from math import log2


np.random.seed(42)  # For reproducibility


# 1. DATA: Actual FIFA Ranking Points
# Source: FIFA/Coca-Cola Men's World Ranking
# These points are already Elo-based therefore no conversion is needed

teams_data = {
    # UEFA Path A
    'Italy':                {'rating': 1702.06, 'fifa_rank': 13, 'confederation': 'UEFA'},
    'Wales':                {'rating': 1529.71, 'fifa_rank': 35, 'confederation': 'UEFA'},
    'Northern Ireland':     {'rating': 1366.02, 'fifa_rank': 69, 'confederation': 'UEFA'},
    'Bosnia and Herzegovina': {'rating': 1362.37, 'fifa_rank': 71, 'confederation': 'UEFA'},

    # UEFA Path B
    'Ukraine':              {'rating': 1557.47, 'fifa_rank': 30, 'confederation': 'UEFA'},
    'Poland':               {'rating': 1532.04, 'fifa_rank': 34, 'confederation': 'UEFA'},
    'Sweden':               {'rating': 1487.13, 'fifa_rank': 42, 'confederation': 'UEFA'},
    'Albania':              {'rating': 1401.07, 'fifa_rank': 63, 'confederation': 'UEFA'},

    # UEFA Path C
    'Turkey':               {'rating': 1582.69, 'fifa_rank': 25, 'confederation': 'UEFA'},
    'Slovakia':             {'rating': 1485.65, 'fifa_rank': 44, 'confederation': 'UEFA'},
    'Romania':              {'rating': 1465.78, 'fifa_rank': 49, 'confederation': 'UEFA'},
    'Kosovo':               {'rating': 1308.84, 'fifa_rank': 79, 'confederation': 'UEFA'},

    # UEFA Path D
    'Denmark':              {'rating': 1616.75, 'fifa_rank': 21, 'confederation': 'UEFA'},
    'Czechia':              {'rating': 1487.00, 'fifa_rank': 43, 'confederation': 'UEFA'},
    'Republic of Ireland':  {'rating': 1436.04, 'fifa_rank': 59, 'confederation': 'UEFA'},
    'North Macedonia':      {'rating': 1378.57, 'fifa_rank': 66, 'confederation': 'UEFA'},

    # Intercontinental Bracket 1
    'DR Congo':             {'rating': 1468.22, 'fifa_rank': 48, 'confederation': 'CAF'},
    'Jamaica':              {'rating': 1362.46, 'fifa_rank': 70, 'confederation': 'CONCACAF'},
    'New Caledonia':        {'rating': 1042.62, 'fifa_rank': 150, 'confederation': 'OFC'},

    # Intercontinental Bracket 2
    'Iraq':                 {'rating': 1436.94, 'fifa_rank': 58, 'confederation': 'AFC'},
    'Bolivia':              {'rating': 1330.52, 'fifa_rank': 76, 'confederation': 'CONMEBOL'},
    'Suriname':             {'rating': 1140.54, 'fifa_rank': 123, 'confederation': 'CONCACAF'},
}


# 2. WIN PROBABILITY MODEL
# FIFA's ranking system uses a divisor of 600 (not 400 like classic Elo) which makes probabilities less extreme for large rating differences
# Source: FIFA World Football Elo Ratings methodology

FIFA_DIVISOR = 600  # FIFA uses 600; classic Elo uses 400

def win_probability(rating_a, rating_b):
    """
    Calculate probability of team A winning using FIFA's Elo formula.
    E_A = 1 / (1 + 10^((R_B - R_A) / 600))
    
    For knockout matches (must produce a winner).
    Draws go to extra time/penalties which effectively produce a winner.
    """
    return 1.0 / (1.0 + 10 ** ((rating_b - rating_a) / FIFA_DIVISOR))


# 3. PLAYOFF BRACKET STRUCTURE

# UEFA Paths: Semi-finals → Final (single leg knockout)
# First team listed is the home team
uefa_paths = {
    'Path A': {
        'semi1': ('Wales', 'Bosnia and Herzegovina'),
        'semi2': ('Italy', 'Northern Ireland'),
    },
    'Path B': {
        'semi1': ('Ukraine', 'Sweden'),
        'semi2': ('Poland', 'Albania'),
    },
    'Path C': {
        'semi1': ('Turkey', 'Romania'),
        'semi2': ('Slovakia', 'Kosovo'),
    },
    'Path D': {
        'semi1': ('Denmark', 'North Macedonia'),
        'semi2': ('Czechia', 'Republic of Ireland'),
    },
}

# Intercontinental brackets: Semi-final → Final (neutral venue in Mexico)
intercon_brackets = {
    'Bracket 1': {
        'semi': ('New Caledonia', 'Jamaica'),
        'seed': 'DR Congo',
    },
    'Bracket 2': {
        'semi': ('Bolivia', 'Suriname'),
        'seed': 'Iraq',
    },
}

# Home advantage in FIFA Elo points
# FIFA estimates home advantage at approximately 100 points
HOME_ADVANTAGE = 100
NEUTRAL_ADVANTAGE = 0


# 4. MATCH SIMULATION FUNCTIONS=

def simulate_match(team_a, team_b, home_advantage_a=0):
    """
    Simulate a single knockout match.
    
    1. Look up actual FIFA points for both teams
    2. Add home advantage to team A if applicable
    3. Calculate win probability using Elo formula
    4. Generate random number to determine winner
    
    Returns: name of the winning team
    """
    rating_a = teams_data[team_a]['rating'] + home_advantage_a
    rating_b = teams_data[team_b]['rating']
    prob_a = win_probability(rating_a, rating_b)
    
    # Weighted coin flip: random number < prob_a means team A wins
    if np.random.random() < prob_a:
        return team_a
    else:
        return team_b

def simulate_uefa_path(path_config):
    """
    Simulate one UEFA playoff path:
    - Two semi-finals (home team gets home advantage)
    - One final (slight home advantage to first drawn team)
    Returns the qualifying team.
    """
    winner_semi1 = simulate_match(
        path_config['semi1'][0], path_config['semi1'][1],
        home_advantage_a=HOME_ADVANTAGE
    )
    winner_semi2 = simulate_match(
        path_config['semi2'][0], path_config['semi2'][1],
        home_advantage_a=HOME_ADVANTAGE
    )
    # Final: home advantage decided by draw (we use half the normal advantage)
    winner_final = simulate_match(
        winner_semi1, winner_semi2,
        home_advantage_a=HOME_ADVANTAGE // 2
    )
    return winner_final

def simulate_intercon_bracket(bracket_config):
    """
    Simulate one intercontinental bracket:
    - One semi-final at neutral venue (Mexico)
    - One final at neutral venue (Mexico)
    Returns the qualifying team.
    """
    winner_semi = simulate_match(
        bracket_config['semi'][0], bracket_config['semi'][1],
        home_advantage_a=NEUTRAL_ADVANTAGE
    )
    winner_final = simulate_match(
        bracket_config['seed'], winner_semi,
        home_advantage_a=NEUTRAL_ADVANTAGE
    )
    return winner_final

def simulate_all_playoffs():
    """
    Simulate all 6 remaining qualification spots.
    Returns a tuple of 6 qualifying team names.
    """
    qualifiers = []
    for path_name, path_config in uefa_paths.items():
        qualifiers.append(simulate_uefa_path(path_config))
    for bracket_name, bracket_config in intercon_brackets.items():
        qualifiers.append(simulate_intercon_bracket(bracket_config))
    return tuple(qualifiers)


# 5. RUN MONTE CARLO SIMULATION (10,000 iterations)

N_SIMULATIONS = 10000

print(f"Running {N_SIMULATIONS:,} Monte Carlo simulations...")
print(f"Using actual FIFA Ranking Points (Jan 2026) with divisor={FIFA_DIVISOR}")
print("=" * 60)

all_results = []
qualification_counts = Counter()

for i in range(N_SIMULATIONS):
    result = simulate_all_playoffs()
    all_results.append(result)
    for team in result:
        qualification_counts[team] += 1


# 6. RESULTS

sorted_probs = sorted(qualification_counts.items(), key=lambda x: x[1], reverse=True)

print("\n QUALIFICATION PROBABILITIES")
print("=" * 60)

# Group results by path
path_groups = {
    'UEFA Path A → Group B': ['Italy', 'Wales', 'Northern Ireland', 'Bosnia and Herzegovina'],
    'UEFA Path B → Group F': ['Ukraine', 'Poland', 'Sweden', 'Albania'],
    'UEFA Path C → Group D': ['Turkey', 'Slovakia', 'Romania', 'Kosovo'],
    'UEFA Path D → Group A': ['Denmark', 'Czechia', 'Republic of Ireland', 'North Macedonia'],
    'Intercontinental 1 → Group E': ['DR Congo', 'Jamaica', 'New Caledonia'],
    'Intercontinental 2 → Group H': ['Iraq', 'Bolivia', 'Suriname'],
}

for path_name, teams in path_groups.items():
    print(f"\n {path_name}")
    for team in teams:
        count = qualification_counts.get(team, 0)
        prob = count / N_SIMULATIONS * 100
        rating = teams_data[team]['rating']
        print(f"  {team:30s}: {prob:6.1f}%  (FIFA pts: {rating:.2f})")


# 7. SCENARIO ANALYSIS

result_counts = Counter(all_results)
most_common = result_counts.most_common(5)

print("\n" + "=" * 60)
print(" TOP 5 MOST LIKELY SCENARIOS")
print("=" * 60)

path_labels = ['Path A', 'Path B', 'Path C', 'Path D', 'IC 1', 'IC 2']
for i, (combo, count) in enumerate(most_common, 1):
    prob = count / N_SIMULATIONS * 100
    print(f"\n  Scenario {i} ({prob:.1f}% — occurred {count:,} times):")
    for label, team in zip(path_labels, combo):
        print(f"    {label:8s}: {team}")

n_unique = len(result_counts)
print(f"\n Unique outcomes observed: {n_unique:,} / 2,304 possible")
