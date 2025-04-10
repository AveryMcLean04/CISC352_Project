import pandas as pd
import json
from ortools.sat.python import cp_model

"""
The constrant solver so far, it takes in an abbreviation from the user and creates all feasible lineups based 
on the constraints, it outputs them all to the terminal and says how many solutions it found.
"""
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

#Can only deal with integers so we map the positions to numbers for the solver
pos_to_num = {"PG": 1, "SG": 2, "SF": 3, "PF": 4, "C": 5}
player_list = list(top12["Player"])

#getting all the players stats on a specified team.
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
# centers_selected = 0
# #loop through all players and check if they are centers
# for p in player_list:
#     if player_vars[p]["Pos"] == 5:
#         centers_selected += player_in[p]
# #adding the constraint
# model.add(centers_selected >= 1)

#want to have 2 "wings", I am counting SG, SF and PF as wings for the time being
wings = 0
for p in player_list:
    if player_vars[p]["Pos"] == 2 or player_vars[p]["Pos"] == 3 or player_vars[p]["Pos"] == 4:
        wings += player_in[p]
model.add(wings >=2)


#making sure the lineup has 2 players who can shoot well 
good_shooters = 0
#adding another player who can shoot at an almost average level
mid_shooters = 0
#loop through all players and check if they have a good enough 3P%
for p in player_list:
    if player_vars[p]["3P%"] >= 0.359:
        good_shooters += player_in[p]
    elif player_vars[p]["3P%"] > 0.34:
        mid_shooters += player_in[p]
#adding the constraints
model.add(good_shooters + mid_shooters >= 2)
# model.add(mid_shooters >= 1)

#I use per 36 minutes stats for some of the constraints because a player getting less minutes may still be a good rebounder/playmaker etc
#but if they play limited minutes their average will be lower so I want to account for that

#lineup must have some rebounders, will be finding each players rebounds/36 minutes
main_rebounders = 0
sec_rebounders = 0
for p in player_list:
    rp36 = (player_vars[p]["REB"] / player_vars[p]["MPG"]) * 36
    if rp36 > 10:
        main_rebounders += player_in[p]
    elif rp36 > 7:
        sec_rebounders += player_in[p]
model.add(main_rebounders + sec_rebounders >= 2)

#must have a couple of players who can pass and create for others
main_playmaker = 0
sec_playmaker = 0
for p in player_list:
    ap36 = (player_vars[p]["AST"] / player_vars[p]["MPG"]) * 36
    if ap36 > 5:
        main_playmaker += player_in[p]
    elif ap36 > 3:
        sec_playmaker += player_in[p]
model.add(main_playmaker + sec_playmaker >= 2)

#want at least 2 quality defenders and one ok defender
good_def = 0
mid_def = 0
for p in player_list:
    #stocks36 is combined steals and blocks per 36 minutes
    stocks36 = ((player_vars[p]["STL"] + player_vars[p]["BLK"]) / player_vars[p]["MPG"]) * 36
    if stocks36 > 2.3:
        good_def += player_in[p]
    elif stocks36 > 1.5:
        mid_def += player_in[p]
model.add(good_def + mid_def >= 3)

solver = cp_model.CpSolver()

# Enumerate all solutions
solution_printer = LineupSolutionPrinter(player_in)
solver.parameters.enumerate_all_solutions = True
status = solver.solve(model, solution_printer)

print(f"\nStatus: {solver.status_name(status)}")
print(f"Total lineups found: {solution_printer.solution_count}")