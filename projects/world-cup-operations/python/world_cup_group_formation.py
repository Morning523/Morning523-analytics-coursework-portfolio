# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 09:25:56 2026
"""

from pulp import *
import pandas as pd

import numpy as np
import pandas as pd
from collections import Counter
from math import log2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

np.random.seed(42)  # For reproducibility


# ============================================================
# DATA: 48 qualifying nations with FIFA points (Jan 2026)
# Source: FIFA/Coca-Cola Men's World Ranking
# ============================================================

# Format: (Nation, Code, Confederation, FIFA Points)
# For 6 TBD playoff nations, we assume: Denmark, Italy, Turkey, Ukraine, Iraq, DR Congo

nations_data = [
    # Pot 1 (Hosts + Top seeds)
    ("Spain", "ESP", "UEFA", 1877.18),
    ("Argentina", "ARG", "CONMEBOL", 1873.33),
    ("France", "FRA", "UEFA", 1870),
    ("England", "ENG", "UEFA", 1834.12),
    ("Brazil", "BRA", "CONMEBOL", 1760.46),
    ("Portugal", "POR", "UEFA", 1760.38),
    ("Netherlands", "NED", "UEFA", 1756.27),
    ("Germany", "GER", "UEFA", 1724.15),
    ("Belgium", "BEL", "UEFA", 1730.71),
    ("USA", "USA", "CONCACAF", 1681.88),       # Host
    ("Mexico", "MEX", "CONCACAF", 1675.75),     # Host
    ("Canada", "CAN", "CONCACAF", 1559.15),     # Host

    # Pot 2
    ("Morocco", "MAR", "CAF", 1736.57),
    ("Colombia", "COL", "CONMEBOL", 1701.3),
    ("Croatia", "CRO", "UEFA", 1716.88),
    ("Senegal", "SEN", "CAF", 1706.83),
    ("Uruguay", "URU", "CONMEBOL", 1672.62),
    ("Switzerland", "SUI", "UEFA", 1654.69),
    ("Japan", "JPN", "AFC", 1650.12),
    ("Iran", "IRN", "AFC", 1617.02),
    ("South Korea", "KOR", "AFC", 1599.45),
    ("Ecuador", "ECU", "CONMEBOL", 1591.73),
    ("Austria", "AUT", "UEFA", 1585.51),
    ("Australia", "AUS", "AFC", 1574.01),

    # Pot 3
    ("Algeria", "ALG", "CAF", 1560.91),
    ("Egypt", "EGY", "CAF", 1556.71),
    ("Norway", "NOR", "UEFA", 1553.14),
    ("Panama", "PAN", "CONCACAF", 1539.47),
    ("Saudi Arabia", "KSA", "AFC", 1429.48),
    ("Tunisia", "TUN", "CAF", 1479.04),
    ("South Africa", "RSA", "CAF", 1432.76),
    ("Qatar", "QAT", "AFC", 1454.96),
    ("Cote d'Ivoire", "CIV", "CAF", 1522.48),
    ("Uzbekistan", "UZB", "AFC", 1462.03),
    ("Scotland", "SCO", "UEFA", 1506.77),
    ("Paraguay", "PAR", "CONMEBOL", 1501.5),

    # Pot 4
    ("Iraq", "IRQ", "AFC", 1436.94),           # Assumed playoff winner (I3)
    ("Ghana", "GHA", "CAF", 1351.09),
    ("Jordan", "JOR", "AFC", 1388.93),
    ("Haiti", "HAI", "CONCACAF", 1294.49),
    ("DR Congo", "COD", "CAF", 1468.22),        # Assumed playoff winner (K2)
    ("New Zealand", "NZL", "OFC", 1279.25),
    ("Cabo Verde", "CPV", "CAF", 1370.49),
    ("Curacao", "CUW", "CONCACAF", 1302.7),
    ("Denmark", "DEN", "UEFA", 1616.75),        # Assumed playoff winner (A4)
    ("Italy", "ITA", "UEFA", 1702.06),          # Assumed playoff winner (B2)
    ("Turkey", "TUR", "UEFA", 1582.69),         # Assumed playoff winner (D4)
    ("Ukraine", "UKR", "UEFA", 1557.47),        # Assumed playoff winner (F3)
]


# PARAMETERS

N = len(nations_data)  # 48 nations
G = 12                 # 12 groups
T = 4                  # 4 teams per group
P = 4                  # 4 pots

assert N == 48, f"Expected 48 nations, got {N}"

# Create indexed data structures
nations = [d[0] for d in nations_data]
codes = {d[0]: d[1] for d in nations_data}
confederations = {d[0]: d[2] for d in nations_data}
points = {d[0]: d[3] for d in nations_data}

# Assign nations to pots based on their position in nations_data
# First 12 = Pot 1 (includes hosts), next 12 = Pot 2, next 12 = Pot 3, last 12 = Pot 4
pots = {}
for i, nation in enumerate(nations):
    pot_num = i // 12 + 1
    pots[nation] = pot_num

# Group indices
groups = list(range(1, G + 1))



# COUNT CONFEDERATIONS

confed_counts = {}
for n in nations:
    c = confederations[n]
    confed_counts[c] = confed_counts.get(c, 0) + 1

print("=" * 60)
print("CONFEDERATION BREAKDOWN")
print("=" * 60)
for c, count in sorted(confed_counts.items(), key=lambda x: -x[1]):
    print(f"  {c}: {count} nations")

print(f"\nWith 12 groups and {confed_counts.get('UEFA', 0)} UEFA nations,")
print(f"  {confed_counts.get('UEFA', 0) - 12} groups must have 2 UEFA nations")

# Print pots
print("\n" + "=" * 60)
print("POT ASSIGNMENTS")
print("=" * 60)
for p in range(1, 5):
    pot_nations = [n for n in nations if pots[n] == p]
    print(f"\nPot {p}:")
    for n in pot_nations:
        print(f"  {n} ({codes[n]}) - {confederations[n]} - {points[n]} pts")


# MODEL
print("\n" + "=" * 60)
print("SOLVING GROUP FORMATION MODEL")
print("=" * 60)

model = LpProblem("GroupFormation2026", LpMaximize)

# Decision variables: x[i][g] = 1 if nation i assigned to group g
x = {}
for i in nations:
    for g in groups:
        x[i, g] = LpVariable(f"x_{codes[i]}_{g}", lowBound=0, upBound=1, cat='Binary')

# Objective variable w (minimum group points)
w = LpVariable("w", lowBound=0)

# OBJECTIVE: Maximise minimum group points (Chebyshev/maximin)
model += w, "Maximise_min_group_points"

# CONSTRAINT (1b): w <= total points in each group
for g in groups:
    model += w <= lpSum(points[i] * x[i, g] for i in nations), f"MinPoints_g{g}"

# CONSTRAINT (1c): Each group has exactly 4 teams
for g in groups:
    model += lpSum(x[i, g] for i in nations) == T, f"GroupSize_g{g}"

# CONSTRAINT (1d): Each nation assigned to exactly one group
for i in nations:
    model += lpSum(x[i, g] for g in groups) == 1, f"OneGroup_{codes[i]}"

# CONSTRAINT (1e): At most 1 nation per pot per group
# Since there are 12 nations per pot and 12 groups, this means exactly 1 per group
for p_num in range(1, P + 1):
    pot_nations = [n for n in nations if pots[n] == p_num]
    for g in groups:
        model += lpSum(x[i, g] for i in pot_nations) <= 1, \
            f"Pot_{p_num}_g{g}"

# CONSTRAINT (1f): At most 1 nation per confederation per group (except UEFA)
for confed in confed_counts:
    if confed == "UEFA":
        continue
    confed_nations = [n for n in nations if confederations[n] == confed]
    for g in groups:
        model += lpSum(x[i, g] for i in confed_nations) <= 1, \
            f"Confed_{confed}_g{g}"

# CONSTRAINT (1g): UEFA nations - at most 2 per group
uefa_nations = [n for n in nations if confederations[n] == "UEFA"]
for g in groups:
    model += lpSum(x[i, g] for i in uefa_nations) <= 2, f"UEFA_max2_g{g}"


# ============================================================
# SOLVE
# ============================================================

solver = PULP_CBC_CMD(msg=1, timeLimit=300)
model.solve(solver)
print(f"\nStatus: {LpStatus[model.status]}")
print(f"Optimal w (min group points): {value(w):.1f}")

# ============================================================
# RESULTS
# ============================================================

group_letters = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F',
                 7:'G', 8:'H', 9:'I', 10:'J', 11:'K', 12:'L'}

print("\n" + "=" * 60)
print("OPTIMAL GROUP FORMATION")
print("=" * 60)

group_points = {}
group_members = {}

for g in groups:
    members = []
    total_pts = 0
    for i in nations:
        if value(x[i, g]) > 0.5:
            members.append((i, codes[i], confederations[i], points[i], pots[i]))
            total_pts += points[i]
    group_points[g] = total_pts
    group_members[g] = members

    print(f"\nGroup {group_letters[g]} (Total: {total_pts} pts)")
    print(f"  {'Nation':<20} {'Code':<6} {'Confed':<12} {'Points':>8} {'Pot':>4}")
    print(f"  {'-'*54}")
    for name, code, confed, pts, pot in sorted(members, key=lambda x: -x[3]):
        print(f"  {name:<20} {code:<6} {confed:<12} {pts:>8.2f} {pot:>4}")

# Summary statistics
all_points = list(group_points.values())
print("\n" + "=" * 60)
print("BALANCE ANALYSIS")
print("=" * 60)
print(f"  Min group points:  {min(all_points):.2f}")
print(f"  Max group points:  {max(all_points):.2f}")
print(f"  Spread:            {max(all_points) - min(all_points):.2f}")
print(f"  Average:           {sum(all_points)/len(all_points):.2f}")
print(f"  Optimal w:         {value(w):.2f}")




# Solve LP relaxation to get meaningful shadow prices
# Relaxing integrality gives valid dual variables for each constraint
print("\n" + "=" * 60)
print("LP RELAXATION - SHADOW PRICES")
print("=" * 60)

lp_model = LpProblem("GroupFormation2026_LP", LpMaximize)

x_lp = {(i, g): LpVariable(f"xlp_{codes[i]}_{g}", lowBound=0, upBound=1) for i in nations for g in groups}
w_lp = LpVariable("w_lp", lowBound=0)

lp_model += w_lp

for g in groups:
    lp_model += w_lp <= lpSum(points[i] * x_lp[i, g] for i in nations), f"MinPoints_g{g}"
    lp_model += lpSum(x_lp[i, g] for i in nations) == T, f"GroupSize_g{g}"

for i in nations:
    lp_model += lpSum(x_lp[i, g] for g in groups) == 1, f"OneGroup_{codes[i]}"

for p_num in range(1, P + 1):
    pot_nations = [n for n in nations if pots[n] == p_num]
    for g in groups:
        lp_model += lpSum(x_lp[i, g] for i in pot_nations) <= 1, f"Pot_{p_num}_g{g}"

for confed in confed_counts:
    if confed == 'UEFA':
        continue
    confed_nations = [n for n in nations if confederations[n] == confed]
    for g in groups:
        lp_model += lpSum(x_lp[i, g] for i in confed_nations) <= 1, f"Confed_{confed}_g{g}"

uefa_nations = [n for n in nations if confederations[n] == 'UEFA']
for g in groups:
    lp_model += lpSum(x_lp[i, g] for i in uefa_nations) <= 2, f"UEFA_max2_g{g}"

lp_model.solve(PULP_CBC_CMD(msg=0))

print("\nShadow prices - confederation constraints (non-zero only):")
for name, constraint in lp_model.constraints.items():
    if ("Confed_" in name or "UEFA_" in name) and constraint.pi != 0:
        print(f"  {name}: {constraint.pi:.4f}")

print("\nShadow prices - pot constraints (non-zero only):")
for name, constraint in lp_model.constraints.items():
    if "Pot_" in name and constraint.pi != 0:
        print(f"  {name}: {constraint.pi:.4f}")

print("\nShadow prices - group size constraints:")
for name, constraint in lp_model.constraints.items():
    if "GroupSize_" in name:
        print(f"  {name}: {constraint.pi:.4f}")
