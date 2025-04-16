"""
DL_prediction.py

This script trains a simple feedforward neural network to predict the adjusted impact
of NBA lineups based on player IDs and home/away team designation. The model uses
embedding layers for lineup representation and outputs adjusted impact scores per
lineup, which are saved for each team.

Techniques used:
- Embedding layer to encode player identities
- Home/Away flag as input feature
- MSE loss with adjusted per-36-minute scaling
- Output includes best/worst starting lineups and top-performing non-starting lineups
"""

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import ast
from torch.nn.utils.rnn import pad_sequence
from collections import defaultdict, Counter

# ---------------------- Constants & Data Preprocessing ----------------------

epsilon = 1e-6
abbrs = ["ATL", "BOS", "BRK", "CHO", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", "HOU", "IND",
         "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", "OKC", "ORL", "PHI", "PHO",
         "POR", "SAC", "SAS", "TOR", "UTA", "WAS"]

# Load data
data = pd.read_csv('Deep Learning/lineup_performance.csv')
data['Impact per 36'] = (data['Net Impact'] / (data['Minutes Played'] + epsilon)) * 36
data['Impact per 36'] = data['Impact per 36'].clip(-40, 40)

# ---------------------- Model Definition ----------------------

class Net(nn.Module):
    """
    Simple feedforward neural network with an embedding layer for player IDs
    and a flag for home/away.
    """
    def __init__(self, num_players, embedding_dim, hidden_size, output_size):
        super(Net, self).__init__()
        self.embeddings = nn.Embedding(num_players, embedding_dim, padding_idx=0)
        self.fc1 = nn.Linear(embedding_dim + 1, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, lineup):
        embedded_lineup = self.embeddings(lineup[:, :-1])
        home_away_info = lineup[:, -1].float().unsqueeze(-1)
        embedded_lineup = embedded_lineup.sum(dim=1)
        combined = torch.cat((embedded_lineup, home_away_info), dim=-1)
        x = self.fc1(combined)
        x = self.relu(x)
        return self.fc2(x)

def lineup_to_indices(lineup, player_to_index, is_home):
    """
    Converts a lineup and team info into player indices + home/away flag.
    """
    lineup_indices = [player_to_index[player] for player in lineup]
    home_away_info = [1 if is_home else 0]
    return lineup_indices + home_away_info

# ---------------------- Starting Lineup Detection ----------------------

# Extract starting lineups (first home and away entries for each game)
starting_lineups = []
for game_id, game_data in data.groupby('GameID'):
    home_lineup, away_lineup = None, None
    for _, row in game_data.iterrows():
        lineup = ast.literal_eval(row['Lineup'])
        if row['Team'] == 'Away' and away_lineup is None:
            away_lineup = lineup
        if row['Team'] == 'Home' and home_lineup is None:
            home_lineup = lineup
        if home_lineup and away_lineup:
            break
    if home_lineup and away_lineup:
        starting_lineups.append((game_id, 'Home', home_lineup))
        starting_lineups.append((game_id, 'Away', away_lineup))

# Filter starting lineups with at least 3 appearances
lineup_counts = Counter(tuple(sorted(lineup)) for _, _, lineup in starting_lineups)
lineup_threshold = 3
valid_lineups = [lineup for lineup, count in lineup_counts.items() if count >= lineup_threshold]
filtered_starting_lineups = [
    (game_id, team, lineup)
    for game_id, team, lineup in starting_lineups
    if tuple(sorted(lineup)) in valid_lineups
]

# ---------------------- Prepare Training Data ----------------------

all_players = sorted(set(player for lineup_str in data['Lineup'] for player in ast.literal_eval(lineup_str)))
player_to_index = {player: idx + 1 for idx, player in enumerate(all_players)}  # reserve 0 for padding

X_train = [
    torch.tensor(lineup_to_indices(ast.literal_eval(row['Lineup']), player_to_index, row['Team'] == 'Home'), dtype=torch.long)
    for _, row in data.iterrows()
]
X_train = pad_sequence(X_train, batch_first=True, padding_value=0)
y_train = torch.tensor(list(data['Impact per 36']), dtype=torch.float32).reshape(-1, 1)

# ---------------------- Train the Model ----------------------

input_size = len(all_players) + 1
embedding_dim, hidden_size, output_size = 16, 32, 1

model = Net(input_size, embedding_dim, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

for epoch in range(500):
    y_pred = model(X_train)
    loss = criterion(y_pred, y_train)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 20 == 0:
        print(f'Epoch [{epoch + 1}/500], Loss: {loss.item():.4f}')

# ---------------------- Lineup Prediction ----------------------

lineup_to_rows = defaultdict(list)
for _, row in data.iterrows():
    lineup = tuple(sorted(ast.literal_eval(row['Lineup'])))
    lineup_to_rows[lineup].append(row)

unique_predictions = []
with torch.no_grad():
    for lineup_tuple, rows in lineup_to_rows.items():
        total_games = len(set(row['GameID'] for row in rows))
        total_minutes = sum(row['Minutes Played'] for row in rows)
        abbr = rows[0]['Abbr']
        is_home = rows[0]['Team'] == 'Home'
        lineup = list(lineup_tuple)
        lineup_vector = lineup_to_indices(lineup, player_to_index, is_home)
        lineup_tensor = torch.tensor([lineup_vector], dtype=torch.long)
        lineup_tensor = pad_sequence(lineup_tensor, batch_first=True, padding_value=0)
        predicted_impact_per_36 = model(lineup_tensor).item()
        adjusted_impact = predicted_impact_per_36 * (total_minutes / (total_minutes + 100))
        unique_predictions.append((lineup, adjusted_impact, abbr, total_games, total_minutes, predicted_impact_per_36))

valid_lineup_set = set(tuple(sorted(lineup)) for _, _, lineup in filtered_starting_lineups)
filtered_predictions = [p for p in unique_predictions if tuple(sorted(p[0])) in valid_lineup_set]
filtered_predictions.sort(key=lambda x: x[1], reverse=True)

non_starting_predictions = [
    p for p in unique_predictions
    if tuple(sorted(p[0])) not in valid_lineup_set and p[3] >= 5
]
non_starting_predictions.sort(key=lambda x: x[1], reverse=True)


# ---------------------- Output Formatting ----------------------

def write_team_lineups_for_abbrs(filtered_predictions, non_starting_predictions, abbrs, output_filename='lineup_predictions.txt'):
    """
    Writes top predicted lineups to file for each team:
    - Top 3 starting lineups
    - Bottom 3 starting lineups
    - Top 3 non-starting lineups (min 5 games)
    """
    team_lineups = defaultdict(lambda: {'best': [], 'worst': [], 'non_starting': []})
    for team in abbrs:
        team_starting = [p for p in filtered_predictions if p[2] == team]
        team_starting.sort(key=lambda x: x[1], reverse=True)
        team_lineups[team]['best'] = team_starting[:3]
        team_lineups[team]['worst'] = team_starting[-3:]

        team_non_starting = [p for p in non_starting_predictions if p[2] == team]
        team_lineups[team]['non_starting'] = team_non_starting[:3]

    with open(output_filename, 'w') as f:
        for team, lineups in team_lineups.items():
            f.write(f"Team: {team}\n")
            f.write("=== Best Predicted Starting Lineups ===\n")
            for lineup, impact, abbr, games, minutes, per36 in lineups['best']:
                f.write(f"Adjusted Impact: {impact:.2f} | Per 36: {per36:.2f} | Games: {games} | Minutes: {minutes:.1f} | Lineup: {', '.join(lineup)}\n")
            f.write("=== Worst Predicted Starting Lineups ===\n")
            for lineup, impact, abbr, games, minutes, per36 in lineups['worst']:
                f.write(f"Adjusted Impact: {impact:.2f} |  Per 36: {per36:.2f} | Games: {games} | Minutes: {minutes:.1f} | Lineup: {', '.join(lineup)}\n")
            f.write("=== Best Predicted Non-Starting Lineups (Min 5 Games) ===\n")
            for lineup, impact, abbr, games, minutes, per36 in lineups['non_starting']:
                f.write(f"Adjusted Impact: {impact:.2f} |  Per 36: {per36:.2f} | Games: {games} | Minutes: {minutes:.1f} | Lineup: {', '.join(lineup)}\n")
            f.write("\n\n")

write_team_lineups_for_abbrs(filtered_predictions, non_starting_predictions, abbrs, output_filename='Deep Learning/lineup_predictions.txt')
print("Finished! Info output to lineup_predictions.txt.")
