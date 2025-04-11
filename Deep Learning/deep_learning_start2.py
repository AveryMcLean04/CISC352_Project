import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import ast
from torch.nn.utils.rnn import pad_sequence
from collections import defaultdict

# Load data
data = pd.read_csv('Deep Learning/lineup_performance.csv')

# Add epsilon to avoid division by zero
epsilon = 1e-6

# Calculate Impact per 36 minutes
data['Impact per 36'] = (data['Net Impact'] / (data['Minutes Played'] + epsilon)) * 36
data['Impact per 36'] = data['Impact per 36'].clip(-40, 40)  # reasonable upper/lower bound


# Define the neural network model
class Net(nn.Module):
    def __init__(self, num_players, embedding_dim, hidden_size, output_size):
        super(Net, self).__init__()
        self.embeddings = nn.Embedding(num_players, embedding_dim, padding_idx=0)  # Set padding_idx=0
        self.fc1 = nn.Linear(embedding_dim + 1, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, lineup):
        embedded_lineup = self.embeddings(lineup[:, :-1])
        home_away_info = lineup[:, -1].float().unsqueeze(-1)

        embedded_lineup = embedded_lineup.sum(dim=1)
        embedded_lineup = torch.cat((embedded_lineup, home_away_info), dim=-1)

        x = self.fc1(embedded_lineup)
        x = self.relu(x)
        x = self.fc2(x)
        return x


def lineup_to_indices(lineup, player_to_index, is_home):
    lineup_indices = [player_to_index[player] for player in lineup]
    home_away_info = [1 if is_home else 0] * len(lineup)
    return lineup_indices + home_away_info


# Initialize a list to store the starting lineups
starting_lineups = []

# Loop through each GameID to extract the starting lineups for both Home and Away teams
for game_id, game_data in data.groupby('GameID'):
    home_lineup = None
    away_lineup = None

    # Find the first Home and Away lineup in each game
    for _, row in game_data.iterrows():
        if row['Team'] == 'Away' and away_lineup is None:
            away_lineup = ast.literal_eval(row['Lineup'])
        if row['Team'] == 'Home' and home_lineup is None:
            home_lineup = ast.literal_eval(row['Lineup'])

        # Once both lineups are found, break the loop
        if home_lineup and away_lineup:
            break

    # Store the lineups if both are found
    if home_lineup and away_lineup:
        starting_lineups.append((game_id, 'Home', home_lineup))
        starting_lineups.append((game_id, 'Away', away_lineup))

lineup_counts = {}
for _, team, lineup in starting_lineups:
    lineup_tuple = tuple(sorted(lineup))
    if lineup_tuple in lineup_counts:
        lineup_counts[lineup_tuple] += 1
    else:
        lineup_counts[lineup_tuple] = 1

lineup_threshold = 15

valid_lineups = [lineup for lineup, count in lineup_counts.items() if count >= lineup_threshold]

filtered_starting_lineups = [(game_id, team, lineup) for game_id, team, lineup in starting_lineups if tuple(sorted(lineup)) in valid_lineups]

# Get all unique players from the season
all_players = set()
for lineup_str in data['Lineup']:
    lineup = ast.literal_eval(lineup_str)
    all_players.update(lineup)
all_players = sorted(list(all_players))
print(f"\nTotal unique players in season: {len(all_players)}")

player_to_index = {player: idx + 1 for idx, player in enumerate(all_players)}  # Shift index by +1 (0 is padding)

# Prepare training data
X_train = [
    lineup_to_indices(ast.literal_eval(row['Lineup']), player_to_index, row['Team'] == 'Home') 
    for _, row in data.iterrows()
]
y_train = list(data['Impact per 36'])

# Convert to PyTorch tensors and pad sequences
X_train = [torch.tensor(x, dtype=torch.long) for x in X_train]
X_train = pad_sequence(X_train, batch_first=True, padding_value=0)  # Pad sequences
y_train = torch.tensor(y_train, dtype=torch.float32).reshape(-1, 1)

# Model parameters
input_size = len(all_players) + 1  # +1 because we added padding index
embedding_dim = 16
hidden_size = 32  
output_size = 1

# Create the model
model = Net(input_size, embedding_dim, hidden_size, output_size)

# Loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Training loop
num_epochs = 500
for epoch in range(num_epochs):
    y_pred = model(X_train)  # Corrected batch input
    loss = criterion(y_pred, y_train)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 20 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# After training, let's evaluate all lineups
regular_predictions = []
with torch.no_grad():
    for _, row in data.iterrows():
        lineup = ast.literal_eval(row['Lineup'])
        actual_impact = row['Impact per 36']

        lineup_vector = lineup_to_indices(lineup, player_to_index, row['Team'] == 'Home')
        lineup_tensor = torch.tensor([lineup_vector], dtype=torch.long)
        lineup_tensor = pad_sequence(lineup_tensor, batch_first=True, padding_value=0)  # Pad sequence

        predicted_impact = model(lineup_tensor).item()

        regular_predictions.append((lineup, predicted_impact))

regular_predictions.sort(key=lambda x: x[1], reverse=True)

# Get the starting lineups for filtering
valid_lineup_set = set(tuple(sorted(lineup)) for _, team, lineup in filtered_starting_lineups)

# Evaluate on all lineups (not just the starting ones)
unique_lineups = set()
unique_predictions = []

with torch.no_grad():
    for _, row in data.iterrows():
        lineup = ast.literal_eval(row['Lineup'])
        actual_impact = row['Impact per 36']

        lineup_vector = lineup_to_indices(lineup, player_to_index, row['Team'] == 'Home')
        lineup_tensor = torch.tensor([lineup_vector], dtype=torch.long)
        lineup_tensor = pad_sequence(lineup_tensor, batch_first=True, padding_value=0)  # Pad sequence

        predicted_impact = model(lineup_tensor).item()

        lineup_tuple = tuple(sorted(lineup))
        if lineup_tuple not in unique_lineups:
            unique_lineups.add(lineup_tuple)
            unique_predictions.append((lineup, predicted_impact, row['Team'], row['GameID']))

filtered_predictions = [prediction for prediction in unique_predictions if tuple(sorted(prediction[0])) in valid_lineup_set]
filtered_predictions.sort(key=lambda x: x[1], reverse=True)

print("\n=== Best Predicted Starting Lineups ===")
for lineup, impact, team, game_id in filtered_predictions[:5]:
    print(f"Impact: {impact:.2f} | Lineup: {', '.join(lineup)}")

print("\n=== Worst Predicted Starting Lineups ===")
for lineup, impact, team, game_id in filtered_predictions[-5:]:
    print(f"Impact: {impact:.2f} | Lineup: {', '.join(lineup)}")
