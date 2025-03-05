import pandas as pd

# Load the original CSV file
df = pd.read_csv("all_games.csv", encoding="ISO-8859-1", delimiter=",", on_bad_lines='skip')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

# Filter the data for the 2021-2022 season (after August 2021 and before July 2022)
df_2021_22 = df[((df['Date'].dt.year == 2021) & (df['Date'].dt.month >= 9)) |  # After August 2021
                ((df['Date'].dt.year == 2022) & (df['Date'].dt.month <= 6))]  # Before July 2022

# Save the filtered data to a new CSV file
df_2021_22.to_csv('filtered_2021_22_season.csv', index=False)

print("Filtered data saved to 'filtered_2021_22_season.csv'")
