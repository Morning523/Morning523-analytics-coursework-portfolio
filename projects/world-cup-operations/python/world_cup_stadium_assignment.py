from pathlib import Path
import pandas as pd
import re
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

FILE = str(Path(__file__).resolve().parents[3] / "data" / "Q3.xlsx")

df_ranking = pd.read_excel(FILE, sheet_name='Ranking')
df_jr      = pd.read_excel(FILE, sheet_name='jr', header=None)  # header=None keeps r=1
df_stadium = pd.read_excel(FILE, sheet_name='Capacity', header=None)

print(df_ranking.head())
print(df_jr.head())

# ---------------------------------------------
# 1. PARSE STADIUMS
# ---------------------------------------------
stadiums = []
for _, row in df_stadium.iterrows():
    name, cap = row.iloc[0], row.iloc[1]
    if pd.notna(name) and pd.notna(cap) and isinstance(cap, (int, float)):
        stadiums.append({'name': str(name).strip(), 'capacity': int(cap)})
stadiums.sort(key=lambda x: x['capacity'], reverse=True)
S = len(stadiums)

print("\n=== STADIUMS ===")
for i, s in enumerate(stadiums):
    print(f"  {i+1:>2}. {s['name']:<35} Capacity: {s['capacity']:,}")

# ---------------------------------------------
# 2. RE-SOLVE Q3 TO GET y[r] VALUES
# ---------------------------------------------
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
assert R == S, f"R={R} must equal S={S}"
print(f"\nR={R} row-sets, S={S} stadiums")

N_z     = G * L
N_y     = R
N_total = N_z + N_y + 1 + 1 + R

def idx_z(g, l): return g * L + l
def idx_y(r):    return N_z + r
IDX_WMIN = N_z + N_y
IDX_WMAX = N_z + N_y + 1
def idx_v(r):    return N_z + N_y + 2 + r

c3 = np.zeros(N_total)
c3[IDX_WMIN] = -1.0
c3[IDX_WMAX] = -1.0

integrality3 = np.zeros(N_total)
for g in range(G):
    for l in range(L): integrality3[idx_z(g, l)] = 1
for r in range(R):    integrality3[idx_v(r)] = 1

lb3 = np.zeros(N_total)
ub3 = np.ones(N_total)
ub3[IDX_WMIN] = ub3[IDX_WMAX] = np.inf
for r in range(R): ub3[idx_y(r)] = np.inf

BIG_M = 20.0
AR, BL, BU = [], [], []
for r in range(R):
    row = np.zeros(N_total); row[IDX_WMIN] = 1; row[idx_y(r)] = -1
    AR.append(row); BL.append(-np.inf); BU.append(0)
for r in range(R):
    row = np.zeros(N_total); row[IDX_WMAX] = -1; row[idx_y(r)] = 1
    AR.append(row); BL.append(-np.inf); BU.append(0)
for r in range(R):
    row = np.zeros(N_total); row[IDX_WMAX] = 1; row[idx_y(r)] = -1; row[idx_v(r)] = BIG_M
    AR.append(row); BL.append(-np.inf); BU.append(BIG_M)
row = np.zeros(N_total)
for r in range(R): row[idx_v(r)] = 1
AR.append(row); BL.append(1); BU.append(1)
for rs in row_sets:
    r = rs['r']; row = np.zeros(N_total); row[idx_y(r)] = 1
    for (letter, qi1, qi2) in rs['matches']:
        l = label_to_g[letter]; pair = (qi1, qi2) if qi1 < qi2 else (qi2, qi1)
        for g in range(G):
            if pair in p_match[g]: row[idx_z(g, l)] -= p_match[g][pair]
    AR.append(row); BL.append(0); BU.append(0)
for l in range(L):
    row = np.zeros(N_total)
    for g in range(G): row[idx_z(g, l)] = 1
    AR.append(row); BL.append(1); BU.append(1)
for g in range(G):
    row = np.zeros(N_total)
    for l in range(L): row[idx_z(g, l)] = 1
    AR.append(row); BL.append(1); BU.append(1)
# (2i) Three host nation constraints for 2026:
#   MEX -> Group A (letter index 0)
#   CAN -> Group B (letter index 1)
#   USA -> Group D (letter index 3)
host_assignments = [
    ('MEX', 0),   # Group A
    ('CAN', 1),   # Group B
    ('USA', 3),   # Group D
]
for code, letter_idx in host_assignments:
    g_idx = next(g for g in range(G) if any(t['code'] == code for t in subsets[g]))
    row = np.zeros(N_total); row[idx_z(g_idx, letter_idx)] = 1
    AR.append(row); BL.append(1); BU.append(1)

print("Solving Q3 (to obtain y[r])...")
res3 = milp(c3,
            constraints=LinearConstraint(np.array(AR), np.array(BL), np.array(BU)),
            integrality=integrality3,
            bounds=Bounds(lb3, ub3),
            options={'disp': False, 'time_limit': 120})

y_opt = np.array([res3.x[idx_y(r)] for r in range(R)])
print(f"Q3 objective (w_min + w_max) = {-res3.fun:.4f}")
print(f"w_min = {res3.x[IDX_WMIN]:.4f},  w_max = {res3.x[IDX_WMAX]:.4f}")

# ---------------------------------------------
# 3. BUILD AND SOLVE Q4
# ---------------------------------------------
N4 = R * S
def idx_a(r, s): return r * S + s

# Minimise -sum capacity[s]*y[r]*a[r,s]
c4 = np.zeros(N4)
for r in range(R):
    for s in range(S):
        c4[idx_a(r, s)] = -stadiums[s]['capacity'] * y_opt[r]

integrality4 = np.ones(N4)
bounds4      = Bounds(lb=np.zeros(N4), ub=np.ones(N4))

A4, B4l, B4u = [], [], []
for r in range(R):   # each row-set to exactly one stadium
    row = np.zeros(N4)
    for s in range(S): row[idx_a(r, s)] = 1
    A4.append(row); B4l.append(1); B4u.append(1)
for s in range(S):   # each stadium hosts exactly one row-set
    row = np.zeros(N4)
    for r in range(R): row[idx_a(r, s)] = 1
    A4.append(row); B4l.append(1); B4u.append(1)

print("\nSolving Q4 (stadium assignment)...")
res4 = milp(c4,
            constraints=LinearConstraint(np.array(A4), np.array(B4l), np.array(B4u)),
            integrality=integrality4,
            bounds=bounds4,
            options={'disp': False, 'time_limit': 60})

print(f"Solver status: {res4.status} - {res4.message}")
print(f"Total popularity value: {-res4.fun:,.2f}")

# ---------------------------------------------
# 4. PRINT RESULTS
# ---------------------------------------------
x4      = res4.x
results = []
for r in range(R):
    for s in range(S):
        if x4[idx_a(r, s)] > 0.5:
            results.append({
                'r':        row_sets[r]['r'] + 1,
                'y':        y_opt[r],
                'stadium':  stadiums[s]['name'],
                'capacity': stadiums[s]['capacity'],
                'pv':       stadiums[s]['capacity'] * y_opt[r]
            })
results.sort(key=lambda x: x['pv'], reverse=True)

print(f"\n{'Row-set':<9} {'Popularity':>12}  {'Stadium':<36} {'Capacity':>10}  {'Pop. Value':>14}")
print("-" * 92)
for res in results:
    print(f"  r={res['r']:<5} {res['y']:>10.4f}  {res['stadium']:<36} {res['capacity']:>10,}  {res['pv']:>14,.2f}")
print("-" * 92)
print(f"{'Total':>63}  {sum(r['pv'] for r in results):>14,.2f}")
