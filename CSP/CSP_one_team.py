"""
CSP Lineup Generator – NBA Team Optimizer

This script uses the OR-Tools CP-SAT solver to generate valid 5-man NBA lineups for a chosen team,
based on constraints such as position balance, shooting ability, rebounding, playmaking, and defense.

Author: Avery McLean
"""

import pandas as pd
import json
from ortools.sat.python import cp_model

# Mapping of team abbreviations to full names for user-friendliness
team_abbreviations = {
    "ATL": "Atlanta Hawks", "BOS": "Boston Celtics", "BRK": "Brooklyn Nets", "CHI": "Chicago Bulls",
    "CHO": "Charlotte Hornets", "CLE": "Cleveland Cavaliers", "DAL": "Dallas Mavericks", "DEN": "Denver Nuggets",
    "DET": "Detroit Pistons", "GSW": "Golden State Warriors", "HOU": "Houston Rockets", "IND": "Indiana Pacers",
    "LAC": "LA Clippers", "LAL": "LA Lakers", "MEM": "Memphis Grizzlies", "MIA": "Miami Heat",
    "MIL": "Milwaukee Bucks", "MIN": "Minnesota Timberwolves", "NOP": "New Orleans Pelicans", "NYK": "New York Knicks",
    "OKC": "Oklahoma City Thunder", "ORL": "Orlando Magic", "PHI": "Philadelphia 76ers", "PHO": "Phoenix Suns",
    "POR": "Portland Trail Blazers", "SAC": "Sacramento Kings", "SAS": "San Antonio Spurs", "TOR": "Toronto Raptors",
    "UTA": "Utah Jazz", "WAS": "Washington Wizards"
}

# Display all valid team abbreviations
print("Available Team Abbreviations:")
for abbr, name in sorted(team_abbreviations.items()):
    print(f"{abbr} - {name}")

# Prompt user to enter a team abbreviation
team_name = input("\nEnter a team (abbr.): ")

# Load dataset
df = pd.read_csv("CSP/2021-2022 NBA Player Stats - Regular.csv", encoding="ISO-8859-1", delimiter=";")

# Filter top 12 players by points, minimum games and points per game
top12 = (
    df[(df["Tm"] == team_name) & (df["G"] > 10) & (df["PTS"] > 3)]
    .sort_values(by="PTS", ascending=False).head(12)
)

# Position to numeric mapping
pos_to_num = {"PG": 1, "SG": 2, "SF": 3, "PF": 4, "C": 5}
player_list = list(top12["Player"])

# Create dictionary of player stats
player_vars = {
    row["Player"]: {
        "Pos": pos_to_num.get(row["Pos"], -1),
        "PTS": row["PTS"],
        "AST": row["AST"],
        "REB": row["TRB"],
        "MPG": row["MP"],
        "3PA": row["3PA"],
        "3P%": row["3P%"],
        "FT%": row["FT%"],
        "STL": row["STL"],
        "BLK": row["BLK"],
        "eFG%": row["eFG%"],
    }
    for _, row in top12.iterrows()
}

# Show the player data
print("\nPlayer Data (Indexed):")
print(json.dumps(player_vars, indent=4))

# ---------------- CP-SAT Model ---------------- #

class LineupSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Callback class for collecting and printing all valid lineups."""
    def __init__(self, variables):
        super().__init__()
        self.__variables = variables
        self.__solution_count = 0
        self.lineups = []

    def on_solution_callback(self):
        self.__solution_count += 1
        lineup = [p for p in self.__variables if self.Value(self.__variables[p]) == 1]
        self.lineups.append(lineup)
        print(f"\nSolution {self.__solution_count}: {lineup}")

    @property
    def solution_count(self):
        return self.__solution_count

# Initialize model
model = cp_model.CpModel()
player_in = {player: model.NewBoolVar(player) for player in player_list}

# Must select exactly 5 players
model.Add(sum(player_in.values()) == 5)

# Wings constraint (SG, SF, PF)
wings = sum(player_in[p] for p in player_list if player_vars[p]["Pos"] in [2, 3, 4])
model.Add(wings >= 2)

# Shooting constraint
good_shooters = 0
mid_shooters = 0
for p in player_list:
    if player_vars[p]["3P%"] >= 0.359:
        good_shooters += player_in[p]
    elif player_vars[p]["3P%"] > 0.34:
        mid_shooters += player_in[p]
model.Add(good_shooters + mid_shooters >= 2)

# Rebounding constraint
main_rebounders = 0
sec_rebounders = 0
for p in player_list:
    rp36 = (player_vars[p]["REB"] / player_vars[p]["MPG"]) * 36
    if rp36 > 10:
        main_rebounders += player_in[p]
    elif rp36 > 7:
        sec_rebounders += player_in[p]
model.Add(main_rebounders + sec_rebounders >= 2)

# Playmaking constraint
main_playmaker = 0
sec_playmaker = 0
for p in player_list:
    ap36 = (player_vars[p]["AST"] / player_vars[p]["MPG"]) * 36
    if ap36 > 5:
        main_playmaker += player_in[p]
    elif ap36 > 3:
        sec_playmaker += player_in[p]
model.Add(main_playmaker + sec_playmaker >= 2)

# Defense constraint
good_def = 0
mid_def = 0
for p in player_list:
    stocks36 = ((player_vars[p]["STL"] + player_vars[p]["BLK"]) / player_vars[p]["MPG"]) * 36
    if stocks36 > 2.3:
        good_def += player_in[p]
    elif stocks36 > 1.5:
        mid_def += player_in[p]
model.Add(good_def + mid_def >= 3)

# Solve model
solver = cp_model.CpSolver()
solution_printer = LineupSolutionPrinter(player_in)
solver.parameters.enumerate_all_solutions = True

status = solver.Solve(model, solution_printer)

print(f"\nStatus: {solver.StatusName(status)}")
print(f"Total lineups found: {solution_printer.solution_count}")

# ---------------- Metric Ranking ---------------- #

def calculate_metric(lineup, metric):
    """Returns the total value for a given metric (PTS, REB, etc.) across the lineup."""
    if metric == 'DEF':
        return sum(player_vars[p]['STL'] + player_vars[p]['BLK'] for p in lineup)
    return sum(player_vars[p][metric] for p in lineup)

# Collect scores
metrics = {'PTS': [], 'REB': [], 'AST': [], 'DEF': []}
for lineup in solution_printer.lineups:
    for metric in metrics:
        value = calculate_metric(lineup, metric)
        metrics[metric].append((lineup, value))

# ---------------- Display Top Lineups ---------------- #

print("\n" + "=" * 40)
print("TOP 5 LINEUPS FOR", team_name)
print("=" * 40)

for metric, lineups_metric in metrics.items():
    print(f"\nTop 5 Lineups by {metric}:")
    top5 = sorted(lineups_metric, key=lambda x: x[1], reverse=True)

    seen = set()
    count = 0
    for lineup, value in top5:
        lineup_tuple = tuple(sorted(lineup))
        if lineup_tuple not in seen:
            seen.add(lineup_tuple)
            count += 1
            print(f"{count}. {', '.join(lineup)} - {value:.2f}")
        if count == 5:
            break
