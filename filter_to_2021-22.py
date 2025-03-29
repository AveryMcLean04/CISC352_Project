import pandas as pd

"""
Takes a massive CSV file and filters it down to contain only the game data for the 2021-22 season.
It then sorts the data by game date (earliest first), and by play number within each game,
and stores it in a file called sorted_filtered_2021_22_season.csv.
As of RIGHT NOW sorted_filtered_2021_22_season.csv is the file i am working from, it to my knowledge has all the information 
in the correct format.
"""

# Load the original CSV file
df = pd.read_csv("all_games.csv", encoding="ISO-8859-1", delimiter=",", on_bad_lines='skip')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Filter the data for the 2021-2022 season (after August 2021 and before July 2022)
df_2021_22 = df[((df['Date'].dt.year == 2021) & (df['Date'].dt.month >= 9)) |  # After August 2021
                ((df['Date'].dt.year == 2022) & (df['Date'].dt.month <= 6))]  # Before July 2022

# Sort the data:
# 1. By 'Date' (game start time) in ascending order (earliest dates first)
# 2. By 'GameID' (to group all plays of the same game together) in ascending order
# 3. By 'PlayNum' in ascending order (to keep plays in correct order within each game)
df_sorted = df_2021_22.sort_values(by=['Date', 'GameID', 'PlayNum'], ascending=[True, True, True])

# Save the sorted data to a new CSV file
df_sorted.to_csv('sorted_filtered_2021_22_season.csv', index=False)

print("Filtered and sorted data saved to 'sorted_filtered_2021_22_season.csv'")
