import pandas as pd
import json
from ortools.sat.python import cp_model
from itertools import combinations

class LineupSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Collects all valid lineups."""
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.lineups = []

    def on_solution_callback(self):
        lineup = [p for p in self.__variables if self.Value(self.__variables[p]) == 1]
        self.lineups.append(lineup)

def get_lineups_for_team(team_name, df):
    top12 = (
        df[(df["Tm"] == team_name) & (df["G"] > 10) & (df["PTS"] > 3)]
        .sort_values(by="PTS", ascending=False).head(12)
    )

    pos_to_num = {"PG": 1, "SG": 2, "SF": 3, "PF": 4, "C": 5}
    player_list = list(top12["Player"])

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

    model = cp_model.CpModel()
    player_in = {player: model.NewBoolVar(player) for player in player_list}

    model.Add(sum(player_in.values()) == 5)

    model.Add(sum(player_in[p] for p in player_list if player_vars[p]["Pos"] in [2, 3, 4]) >= 2)
    model.Add(sum(player_in[p] for p in player_list if player_vars[p]["3P%"] >= 0.359) +
              sum(player_in[p] for p in player_list if 0.34 < player_vars[p]["3P%"] < 0.359) >= 2)
    model.Add(sum(player_in[p] for p in player_list if (player_vars[p]["REB"] / player_vars[p]["MPG"]) * 36 > 10) +
              sum(player_in[p] for p in player_list if 7 < (player_vars[p]["REB"] / player_vars[p]["MPG"]) * 36 <= 10) >= 2)
    model.Add(sum(player_in[p] for p in player_list if (player_vars[p]["AST"] / player_vars[p]["MPG"]) * 36 > 5) +
              sum(player_in[p] for p in player_list if 3 < (player_vars[p]["AST"] / player_vars[p]["MPG"]) * 36 <= 5) >= 2)
    model.Add(sum(player_in[p] for p in player_list if ((player_vars[p]["STL"] + player_vars[p]["BLK"]) / player_vars[p]["MPG"]) * 36 > 2.3) +
              sum(player_in[p] for p in player_list if 1.5 < ((player_vars[p]["STL"] + player_vars[p]["BLK"]) / player_vars[p]["MPG"]) * 36 <= 2.3) >= 3)

    solver = cp_model.CpSolver()
    solution_printer = LineupSolutionPrinter(player_in)
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solution_printer)

    return solution_printer.lineups, player_vars


def calculate_metric(lineup, player_vars, metric):
    if metric == 'DEF':
        return sum(player_vars[p]['STL'] + player_vars[p]['BLK'] for p in lineup)
    return sum(player_vars[p][metric] for p in lineup)


df = pd.read_csv("CSP/2021-2022 NBA Player Stats - Regular.csv", encoding="ISO-8859-1", delimiter=";")
teams = df["Tm"].unique()

lineup_counts = {}
output_lines = []

for team in teams:
    print(f"Processing {team}...")
    lineups, player_vars = get_lineups_for_team(team, df)
    lineup_counts[team] = len(lineups)

    metrics = {'PTS': [], 'REB': [], 'AST': [], 'DEF': []}

    for lineup in lineups:
        for metric in metrics.keys():
            value = calculate_metric(lineup, player_vars, metric)
            metrics[metric].append((lineup, value))

    output_lines.append("=" * 40)
    output_lines.append(f"TEAM: {team}")
    output_lines.append("=" * 40)

    for metric, lineups_metric in metrics.items():
        output_lines.append(f"\nTop 5 Lineups by {metric}:")
        top5 = sorted(lineups_metric, key=lambda x: x[1], reverse=True)[:5]
        for i, (lineup, value) in enumerate(top5, start=1):
            output_lines.append(f"{i}. {lineup} - {value:.2f}")

    output_lines.append(f"\nTotal Feasible Lineups Found: {len(lineups)}\n")

avg_lineups = sum(lineup_counts.values()) / len(lineup_counts)
most_lineups_team = max(lineup_counts, key=lineup_counts.get)
least_lineups_team = min(lineup_counts, key=lineup_counts.get)

output_lines.append("=" * 40)
output_lines.append("OVERALL RESULTS")
output_lines.append("=" * 40)
output_lines.append(f"Average number of lineups: {avg_lineups:.2f}")
output_lines.append(f"Most lineups: {most_lineups_team} with {lineup_counts[most_lineups_team]}")
output_lines.append(f"Least lineups: {least_lineups_team} with {lineup_counts[least_lineups_team]}")

with open("CSP/lineup_results.txt", "w") as f:
    f.write("\n".join(output_lines))

print("Finished! Output written to lineup_results.txt")
