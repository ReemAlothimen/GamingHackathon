import random
import csv

# Define the number of players and their skill levels
num_players = 100
min_skill = 1
max_skill = 100

# Create a list to store player data
players = []

# Generate random player data
for player_id in range(num_players):
    player_name = f"Player {player_id + 1}"
    skill_level = random.randint(min_skill, max_skill)
    players.append({"Name": player_name, "XP": skill_level})

# Define the name of the CSV file
csv_file = "player_data.csv"

# Write player data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    fieldnames = ['Name', 'XP']
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    # Write the header row
    writer.writeheader()

    # Write player data
    for player in players:
        writer.writerow(player)

print(f"Player data has been saved to {csv_file}.")
