import pandas as pd
import json
from ortools.sat.python import cp_model
"""
This is the same as my csp_start functionally but it will act for all 30 nba teams, tell me the average number of lineups
that teams make and who had the most and least lineups.
"""

class LineupSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Prints all valid lineups and tracks the count of solutions."""
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1

    @property
    def solution_count(self):
        return self.__solution_count


def get_lineups_for_team(team_name, df):
    # Filtering out players based on given criteria
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

    # Create the model
    model = cp_model.CpModel()

    player_in = {}
    for player in player_list:
        player_in[player] = model.new_bool_var(player)

    total_selected = 0
    for p in player_list:
        total_selected += player_in[p]
    model.add(total_selected == 5)

    wings = 0
    for p in player_list:
        if player_vars[p]["Pos"] == 2 or player_vars[p]["Pos"] == 3 or player_vars[p]["Pos"] == 4:
            wings += player_in[p]
    model.add(wings >= 2)

    # Good shooters and mid shooters
    good_shooters = 0
    mid_shooters = 0
    for p in player_list:
        if player_vars[p]["3P%"] >= 0.359:
            good_shooters += player_in[p]
        elif player_vars[p]["3P%"] > 0.34:
            mid_shooters += player_in[p]
    model.add(good_shooters + mid_shooters >= 2)

    main_rebounders = 0
    sec_rebounders = 0
    for p in player_list:
        rp36 = (player_vars[p]["REB"] / player_vars[p]["MPG"]) * 36
        if rp36 > 10:
            main_rebounders += player_in[p]
        elif rp36 > 7:
            sec_rebounders += player_in[p]
    model.add(main_rebounders + sec_rebounders >= 2)

    main_playmaker = 0
    sec_playmaker = 0
    for p in player_list:
        ap36 = (player_vars[p]["AST"] / player_vars[p]["MPG"]) * 36
        if ap36 > 5:
            main_playmaker += player_in[p]
        elif ap36 > 3:
            sec_playmaker += player_in[p]
    model.add(main_playmaker + sec_playmaker >= 2)

    good_def = 0
    mid_def = 0
    for p in player_list:
        stocks36 = ((player_vars[p]["STL"] + player_vars[p]["BLK"]) / player_vars[p]["MPG"]) * 36
        if stocks36 > 2.3:
            good_def += player_in[p]
        elif stocks36 > 1.5:
            mid_def += player_in[p]
    model.add(good_def + mid_def >= 3)

    # Solving the model
    solver = cp_model.CpSolver()
    solution_printer = LineupSolutionPrinter(player_in)
    solver.parameters.enumerate_all_solutions = True
    status = solver.solve(model, solution_printer)

    return solution_printer.solution_count


# Get all teams from the dataset
df = pd.read_csv("2021-2022 NBA Player Stats - Regular.csv", encoding="ISO-8859-1", delimiter=";")
teams = df["Tm"].unique()

lineup_counts = {}
for team in teams:
    print(f"Processing team: {team}")
    lineup_count = get_lineups_for_team(team, df)
    lineup_counts[team] = lineup_count

# Calculate and print the average, highest, and lowest lineup counts
average_lineups = sum(lineup_counts.values()) / len(lineup_counts)
highest_team = max(lineup_counts, key=lineup_counts.get)
highest_lineups = lineup_counts[highest_team]
lowest_team = min(lineup_counts, key=lineup_counts.get)
lowest_lineups = lineup_counts[lowest_team]

print("\nResults:")
print(f"Average number of lineups: {average_lineups}")
print(f"Team with the highest number of lineups: {highest_team} with {highest_lineups} lineups")
print(f"Team with the lowest number of lineups: {lowest_team} with {lowest_lineups} lineups")
