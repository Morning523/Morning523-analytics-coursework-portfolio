from pathlib import Path
import re
from itertools import product as iproduct
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import csc_matrix
import numpy as np
import pandas as pd

FILE = str(Path(__file__).resolve().parents[3] / "data" / "Q3.xlsx")

df_ranking = pd.read_excel(FILE, sheet_name='Ranking')
df_jr      = pd.read_excel(FILE, sheet_name='jr', header=None)  # header=None keeps r=1

print(df_ranking.head())
print(df_jr.head())

# Map subset label (A-L) -> integer index 0-11
subset_labels = list('ABCDEFGHIJKL')
label_to_g    = {l: i for i, l in enumerate(subset_labels)}

subsets = {g: [] for g in range(12)}
for _, row in df_ranking.iterrows():
    g = label_to_g[row['Group']]
    subsets[g].append({
        'nation': row['Nation'], 'code': row['Code'],
        'pts': row['Points'], 'pot': row['Pot'], 'si': float(row['Spectator_Index'])
    })
for g in range(12):
    subsets[g].sort(key=lambda x: x['pot'])

fi = {}
for g in range(12):
    for idx, team in enumerate(subsets[g]):
        fi[(g, idx + 1)] = team['si']

print("\nSpectator indices per subset:")
for g in range(12):
    print(f"  Subset {subset_labels[g]}: " +
          " | ".join([f"{t['nation']} (SI={t['si']})" for t in subsets[g]]))

def match_popularity(fi1, fi2):
    f_other     = (fi1 + fi2) / 2
    f_officials = 1.0 if max(fi1, fi2) == 1.0 else (fi1 + fi2) / 2
    return fi1 + fi2 + f_other + f_officials

p_match = {}
for g in range(12):
    p_match[g] = {}
    for qi1 in range(1, 5):
        for qi2 in range(qi1 + 1, 5):
            p_match[g][(qi1, qi2)] = match_popularity(fi[(g, qi1)], fi[(g, qi2)])

print("\nMatch popularities (sample - Subset A):")
for (qi1, qi2), pop in p_match[0].items():
    print(f"  ({qi1},{qi2}) {subsets[0][qi1-1]['nation']} vs {subsets[0][qi2-1]['nation']}: {pop:.4f}")

row_sets = []
for _, row in df_jr.iterrows():
    r_idx     = int(row.iloc[0]) - 1
    match_str = str(row.iloc[2])
    found     = re.findall(r'\(([A-L]),(\d),(\d)\)', match_str)
    parsed    = [(letter, int(q1), int(q2)) for letter, q1, q2 in found]
    row_sets.append({'r': r_idx, 'matches': parsed})

R = len(row_sets)
G = 12
L = 12
print(f"\nNumber of row-sets R={R}, Subsets G={G}, Letters L={L}")

N_z     = G * L
N_y     = R
N_total = N_z + N_y + 1 + 1 + R

def idx_z(g, l): return g * L + l
def idx_y(r):    return N_z + r
IDX_WMIN = N_z + N_y
IDX_WMAX = N_z + N_y + 1
def idx_v(r):    return N_z + N_y + 2 + r

c = np.zeros(N_total)
c[IDX_WMIN] = -1.0
c[IDX_WMAX] = -1.0

integrality = np.zeros(N_total)
for g in range(G):
    for l in range(L): integrality[idx_z(g, l)] = 1
for r in range(R):    integrality[idx_v(r)] = 1

lb = np.zeros(N_total)
ub = np.ones(N_total)
ub[IDX_WMIN] = ub[IDX_WMAX] = np.inf
for r in range(R): ub[idx_y(r)] = np.inf

BIG_M = 20.0
AR, BL, BU = [], [], []

for r in range(R):    # (2b) w_min <= y[r]
    row = np.zeros(N_total); row[IDX_WMIN] = 1; row[idx_y(r)] = -1
    AR.append(row); BL.append(-np.inf); BU.append(0)
for r in range(R):    # (2c) w_max >= y[r]
    row = np.zeros(N_total); row[IDX_WMAX] = -1; row[idx_y(r)] = 1
    AR.append(row); BL.append(-np.inf); BU.append(0)
for r in range(R):    # (2d) w_max <= y[r] + M*(1-v[r])
    row = np.zeros(N_total); row[IDX_WMAX] = 1; row[idx_y(r)] = -1; row[idx_v(r)] = BIG_M
    AR.append(row); BL.append(-np.inf); BU.append(BIG_M)
row = np.zeros(N_total)   # (2e) sum v[r] = 1
for r in range(R): row[idx_v(r)] = 1
AR.append(row); BL.append(1); BU.append(1)
for rs in row_sets:   # (2f) y[r] = sum popularity * z
    r = rs['r']; row = np.zeros(N_total); row[idx_y(r)] = 1
    for (letter, qi1, qi2) in rs['matches']:
        l = label_to_g[letter]; pair = (qi1, qi2) if qi1 < qi2 else (qi2, qi1)
        for g in range(G):
            if pair in p_match[g]: row[idx_z(g, l)] -= p_match[g][pair]
    AR.append(row); BL.append(0); BU.append(0)
for l in range(L):    # (2g) sum_g z[g,l] = 1
    row = np.zeros(N_total)
    for g in range(G): row[idx_z(g, l)] = 1
    AR.append(row); BL.append(1); BU.append(1)
for g in range(G):    # (2h) sum_l z[g,l] = 1
    row = np.zeros(N_total)
    for l in range(L): row[idx_z(g, l)] = 1
    AR.append(row); BL.append(1); BU.append(1)

# (2i) Host nation constraints for 2026 (three hosts):
#   MEX subset -> Group A (letter index 0)
#   CAN subset -> Group B (letter index 1)
#   USA subset -> Group D (letter index 3)
host_assignments = [
    ('MEX', 0),   # Group A
    ('CAN', 1),   # Group B
    ('USA', 3),   # Group D
]
for code, letter_idx in host_assignments:
    g_idx = next(g for g in range(G) if any(t['code'] == code for t in subsets[g]))
    row = np.zeros(N_total); row[idx_z(g_idx, letter_idx)] = 1
    AR.append(row); BL.append(1); BU.append(1)
    print(f"Host constraint: {code} (subset {subset_labels[g_idx]}) -> Group {subset_labels[letter_idx]}")

print("\nSolving Q3...\n")
result = milp(c,
              constraints=LinearConstraint(np.array(AR), np.array(BL), np.array(BU)),
              integrality=integrality,
              bounds=Bounds(lb, ub),
              options={'disp': True, 'time_limit': 120})

print(f"\nSolver status: {result.status} - {result.message}")
print(f"Objective (w_min + w_max): {-result.fun:.4f}")

x         = result.x
w_min_val = x[IDX_WMIN]
w_max_val = x[IDX_WMAX]
print(f"w_min = {w_min_val:.4f}")
print(f"w_max = {w_max_val:.4f}")

assignment = {}
for g in range(G):
    for l in range(L):
        if x[idx_z(g, l)] > 0.5:
            assignment[g] = l

print("\n=== GROUP-LETTER ASSIGNMENT ===")
print(f"{'Letter':<8} {'Subset':<8} {'Teams':<65} {'Total Points'}")
print("-" * 105)
for l in range(L):
    g         = next(gg for gg, ll in assignment.items() if ll == l)
    teams_str = " | ".join([f"{t['nation']}(SI={t['si']})" for t in subsets[g]])
    total_pts = sum(t['pts'] for t in subsets[g])
    host_tag  = " *** HOST ***" if any(t['code'] in ['MEX','CAN','USA'] for t in subsets[g]) else ""
    print(f"  {subset_labels[l]:<6} {subset_labels[g]:<8} {teams_str:<65} {total_pts:.2f}{host_tag}")

print("\n=== ROW-SET POPULARITIES ===")
print(f"{'Row-set':<10} {'Matches':<65} {'Popularity'}")
print("-" * 90)
y_vals = []
for rs in row_sets:
    r         = rs['r']
    y_val     = x[idx_y(r)]
    y_vals.append(y_val)
    match_str = ", ".join([f"({m[0]},{m[1]},{m[2]})" for m in rs['matches']])
    print(f"  r={r+1:<6} {match_str:<65} {y_val:.4f}")

print(f"\nMin row-set popularity : {min(y_vals):.4f}  (= w_min)")
print(f"Max row-set popularity : {max(y_vals):.4f}  (= w_max)")
print(f"Mean row-set popularity: {np.mean(y_vals):.4f}")

print("""
=== WHY w_max IS THE MAXIMUM ROW-SET POPULARITY ===

Constraints (2c) force  w_max >= y[r]  for ALL r,
so w_max is an upper bound on every row-set popularity.

Constraints (2d) add  w_max <= y[r] + M*(1 - v[r])  for each r,
and constraint (2e) forces exactly one v[r*] = 1.

  When v[r*] = 1:  w_max <= y[r*] + M*0 = y[r*]
    -> w_max is tightly bound to that row-set's popularity.
  When v[r]  = 0:  w_max <= y[r] + M   (non-binding slack).

Because the objective maximises w_max, the solver drives it as high
as possible. Together with (2c), at optimality: w_max = max_r y[r].

=== MODIFICATION FROM ORIGINAL PAPER ===

The original paper (Qatar 2022) had ONE host nation fixed to Group A.
For 2026, there are THREE host nations with FIFA-specified group assignments:
  - Mexico  -> Group A
  - Canada  -> Group B
  - USA     -> Group D
Constraint (2i) is therefore extended to three separate equality constraints.
""")
