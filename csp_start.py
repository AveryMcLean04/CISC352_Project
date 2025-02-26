import pandas as pd
import json

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

player_to_number = {player: i for i, player in enumerate(top12["Player"])}


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


# print(json.dumps(player_vars, indent=4))

# print(top12)
