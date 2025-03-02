import pandas as pd
import json
from ortools.sat.python import cp_model

class LineupSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Prints all valid lineups."""
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        lineup = [p for p in self.__variables if self.value(self.__variables[p]) == 1]
        print(f"\nSolution {self.__solution_count}: {lineup}")

    @property
    def solution_count(self):
        return self.__solution_count


df = pd.read_csv("2021-2022 NBA Player Stats - Regular.csv", encoding="ISO-8859-1", delimiter=";")

#getting a team from the user
team_name = input("Enter a team (abbr.): ")

#filtering out players that would not play in an ideal scenario, 
# eliminating players who played fewer than 10 games for that team 
# and who averaged fewer than 3 points per game, and then taking the top 12 scorers of the remaining players
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
    }
    for _, row in top12.iterrows()
}

print("\nPlayer Data (Indexed):")
print(json.dumps(player_vars, indent=4))

#creating the model
model = cp_model.CpModel()

#variable for each player, 0 if not selected, 1 is selected
player_in = {}
#loop through player list and create a boolean variable for each one
for player in player_list:
    player_in[player] = model.new_bool_var(player)

#making sure exactly 5 players are selected
#sum variable
total_selected = 0
#loop through all players and add their selection variable to the sum
for p in player_list:
    total_selected += player_in[p]
#add constraint to the model
model.add(total_selected == 5)

#making sure there is always a center on the floor
centers_selected = 0
#loop through all players and check if they are centers
for p in player_list:
    if player_vars[p]["Pos"] == 5:
        centers_selected += player_in[p]
#adding the constraint
model.add(centers_selected >= 1)

solver = cp_model.CpSolver()


# Enumerate all solutions
solution_printer = LineupSolutionPrinter(player_in)
solver.parameters.enumerate_all_solutions = True
status = solver.solve(model, solution_printer)

print(f"\nStatus: {solver.status_name(status)}")
print(f"Total lineups found: {solution_printer.solution_count}")