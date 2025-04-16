import pandas as pd
from datetime import datetime

"""
This script tracks the net ratings and minutes played of each lineup on the court during the 2021-2022 NBA season. 
The net rating is calculated as the difference between points scored and points allowed by each lineup.
Takes sorted_filtered_2021_22_season.csv and gets every lineup for both teams in every game, piping
it into lineup_performance.csv.
"""

df = pd.read_csv("Deep_Learning/sorted_filtered_2021_22_season.csv", encoding="ISO-8859-1", delimiter=",")

# Convert 'Date' column to datetime format for easy comparison
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

lineup_stats = []

previous_game_id = None
previous_period = None

# Tracking variables (reset at the start of each game/quarter)
current_away_lineup = None
current_home_lineup = None
away_score_at_entry_for_away = None
home_score_at_entry_for_away = None
home_score_at_entry_for_home = None
away_score_at_entry_for_home = None
away_entry_time_for_away = None
home_entry_time_for_home = None

def calculate_minutes_played(start_time, end_time):
    """
    Gets the start and end time for each lineup and gets the total 
    minutes played in that shift.
    """
    if start_time is None or end_time is None:
        return 0  # No time data available yet
    try:
        start = datetime.strptime(start_time.split(".")[0], "%M:%S")
        end = datetime.strptime(end_time.split(".")[0], "%M:%S")
        return abs((start - end).total_seconds() / 60)
    except Exception as e:
        print(f"Error calculating minutes played between {start_time} and {end_time}: {e}")
        return 0



for index, row in df.iterrows():
    game_id = row['GameID']
    current_period = row['Period']

    # If new game starts, reset all tracking variables
    if game_id != previous_game_id:
        away_entry_time_for_away = "12:00"
        home_entry_time_for_home = "12:00"

        print(f"Processing new game: {game_id}")
    
        first_row = df[df["GameID"] == game_id].iloc[0]
        current_away_lineup = tuple(sorted([first_row['A1'], first_row['A2'], first_row['A3'], first_row['A4'], first_row['A5']]))
        current_home_lineup = tuple(sorted([first_row['H1'], first_row['H2'], first_row['H3'], first_row['H4'], first_row['H5']]))

        # Reset score tracking
        away_score_at_entry_for_away = first_row['AwayScore']
        home_score_at_entry_for_away = first_row['HomeScore']
        home_score_at_entry_for_home = first_row['HomeScore']
        away_score_at_entry_for_home = first_row['AwayScore']

        previous_game_id = game_id
        previous_period = current_period
    
    # If new quarter starts in the same game, capture the previous lineups' performance and reset
    elif current_period != previous_period:
        away_entry_time_for_away = "12:00"
        home_entry_time_for_home = "12:00"

        print(f"Processing new period: {current_period} in game: {game_id}")
        
        # Record performance of the previous lineups before the quarter break
        points_scored_away = row['AwayScore'] - away_score_at_entry_for_away
        points_allowed_away = row['HomeScore'] - home_score_at_entry_for_away
        net_impact_away = points_scored_away - points_allowed_away

        lineup_stats.append({
            'GameID': row['GameID'],
            'Period': previous_period,  # Use previous period since this is for end of that period
            'Time': "00:00",  # End of quarter
            'Team': 'Away',
            'Abbr': row['AwayName'],
            'Lineup': current_away_lineup,
            'Points Scored': points_scored_away,
            'Points Allowed': points_allowed_away,
            'Net Impact': net_impact_away,
            'Minutes Played': calculate_minutes_played(away_entry_time_for_away, row['Time'])
        })
        
        away_entry_time_for_away = row['Time']

        points_scored_home = row['HomeScore'] - home_score_at_entry_for_home
        points_allowed_home = row['AwayScore'] - away_score_at_entry_for_home
        net_impact_home = points_scored_home - points_allowed_home

        lineup_stats.append({
            'GameID': row['GameID'],
            'Period': previous_period,  # Use previous period since this is for end of that period
            'Time': "00:00",  # End of quarter
            'Team': 'Home',
            'Abbr': row['HomeName'],
            'Lineup': current_home_lineup,
            'Points Scored': points_scored_home,
            'Points Allowed': points_allowed_home,
            'Net Impact': net_impact_home,
            'Minutes Played': calculate_minutes_played(home_entry_time_for_home, row['Time'])

        })
        
        home_entry_time_for_home = row['Time']

        # Get the lineups for the new quarter
        # Find the first row of the new period
        first_row_of_period = df[(df["GameID"] == game_id) & (df["Period"] == current_period)].iloc[0]
        current_away_lineup = tuple(sorted([first_row_of_period['A1'], first_row_of_period['A2'], 
                                           first_row_of_period['A3'], first_row_of_period['A4'], 
                                           first_row_of_period['A5']]))
        current_home_lineup = tuple(sorted([first_row_of_period['H1'], first_row_of_period['H2'], 
                                           first_row_of_period['H3'], first_row_of_period['H4'], 
                                           first_row_of_period['H5']]))

        # Reset score tracking for the new period
        away_score_at_entry_for_away = row['AwayScore']
        home_score_at_entry_for_away = row['HomeScore']
        home_score_at_entry_for_home = row['HomeScore']
        away_score_at_entry_for_home = row['AwayScore']
        
        previous_period = current_period

    # Check if away sub occurred
    away_sub = not pd.isna(row['AwayIn']) or not pd.isna(row['AwayOut'])
    home_sub = not pd.isna(row['HomeIn']) or not pd.isna(row['HomeOut'])

    if away_sub:
        points_scored_away = row['AwayScore'] - away_score_at_entry_for_away
        points_allowed_away = row['HomeScore'] - home_score_at_entry_for_away
        net_impact_away = points_scored_away - points_allowed_away

        lineup_stats.append({
            'GameID': row['GameID'],
            'Period': row['Period'],
            'Time': row['Time'],
            'Team': 'Away',
            'Abbr': row['AwayName'],
            'Lineup': current_away_lineup,
            'Points Scored': points_scored_away,
            'Points Allowed': points_allowed_away,
            'Net Impact': net_impact_away,
            'Minutes Played': calculate_minutes_played(away_entry_time_for_away, row['Time'])

        })

        away_entry_time_for_away = row['Time']

        # Update the lineup for Away using the current row's data
        if not pd.isna(row['AwayIn']):
            # Get the current on-court players
            current_players = []
            for i in range(1, 6):
                player_col = f'A{i}'
                if player_col in row and not pd.isna(row[player_col]):
                    current_players.append(row[player_col])
            
            # If we have 5 players, update the lineup
            if len(current_players) == 5:
                current_away_lineup = tuple(sorted(current_players))
            else:
                print(f"Warning: Incomplete away lineup data at row {index}")

        # Update score tracking **only for the away lineup**
        away_score_at_entry_for_away = row['AwayScore']
        home_score_at_entry_for_away = row['HomeScore']

    if home_sub:
        points_scored_home = row['HomeScore'] - home_score_at_entry_for_home
        points_allowed_home = row['AwayScore'] - away_score_at_entry_for_home
        net_impact_home = points_scored_home - points_allowed_home

        lineup_stats.append({
            'GameID': row['GameID'],
            'Period': row['Period'],
            'Time': row['Time'],
            'Team': 'Home',
            'Abbr': row['HomeName'],
            'Lineup': current_home_lineup,
            'Points Scored': points_scored_home,
            'Points Allowed': points_allowed_home,
            'Net Impact': net_impact_home,
            'Minutes Played': calculate_minutes_played(home_entry_time_for_home, row['Time'])

        })

        home_entry_time_for_home = row['Time']

        # Update the lineup for Home using the current row's data
        if not pd.isna(row['HomeIn']):
            # Get the current on-court players
            current_players = []
            for i in range(1, 6):
                player_col = f'H{i}'
                if player_col in row and not pd.isna(row[player_col]):
                    current_players.append(row[player_col])
            
            # If we have 5 players, update the lineup
            if len(current_players) == 5:
                current_home_lineup = tuple(sorted(current_players))
            else:
                print(f"Warning: Incomplete home lineup data at row {index}")

        # Update score tracking **only for the home lineup**
        home_score_at_entry_for_home = row['HomeScore']
        away_score_at_entry_for_home = row['AwayScore']

# Handle the final lineups of the last game/period
if previous_game_id is not None:
    # Use the last row of the dataset
    last_row = df.iloc[-1]
    
    # Record performance of the final lineups
    points_scored_away = last_row['AwayScore'] - away_score_at_entry_for_away
    points_allowed_away = last_row['HomeScore'] - home_score_at_entry_for_away
    net_impact_away = points_scored_away - points_allowed_away

    lineup_stats.append({
        'GameID': last_row['GameID'],
        'Period': last_row['Period'],
        'Time': "00:00",  # End of game/period
        'Team': 'Away',
        'Abbr': row['AwayName'],
        'Lineup': current_away_lineup,
        'Points Scored': points_scored_away,
        'Points Allowed': points_allowed_away,
        'Net Impact': net_impact_away,
        'Minutes Played': calculate_minutes_played(away_entry_time_for_away, row['Time'])

    })
    
    away_entry_time_for_away = row['Time']

    points_scored_home = last_row['HomeScore'] - home_score_at_entry_for_home
    points_allowed_home = last_row['AwayScore'] - away_score_at_entry_for_home
    net_impact_home = points_scored_home - points_allowed_home

    lineup_stats.append({
        'GameID': last_row['GameID'],
        'Period': last_row['Period'],
        'Time': "00:00",  # End of game/period
        'Team': 'Home',
        'Abbr': row['HomeName'],
        'Lineup': current_home_lineup,
        'Points Scored': points_scored_home,
        'Points Allowed': points_allowed_home,
        'Net Impact': net_impact_home,
        'Minutes Played': calculate_minutes_played(home_entry_time_for_home, row['Time'])

    })
    
    home_entry_time_for_home = row['Time']

# Convert lineup stats into a DataFrame
lineup_df = pd.DataFrame(lineup_stats)
# Save the DataFrame to a CSV file (overwrites previous file)
lineup_df.to_csv("Deep_Learning/lineup_performance.csv", index=False)
print("Lineup performance data saved to 'Deep Learning/lineup_performance.csv'.")