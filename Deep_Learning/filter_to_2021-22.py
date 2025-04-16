import pandas as pd

"""
Takes all_games.csv, filters it donw to the 2021-22 NBA season and outputs that in sorted
chronological order to sorted_filtered_2021-22_season.csv.
"""

# Load the original CSV file
df = pd.read_csv("Deep Learning/all_games.csv", encoding="ISO-8859-1", delimiter=",", on_bad_lines='skip')

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
df_sorted.to_csv('Deep Learning/sorted_filtered_2021_22_season.csv', index=False)

print("Filtered and sorted data saved to 'sorted_filtered_2021_22_season.csv'")
