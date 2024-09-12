import requests
import pandas as pd
import time

# Read fixture IDs from CSV
fixtures = pd.read_csv('fixtures_cleaned.csv')
fixture_ids = fixtures['fixture_id']

# Set up the RapidAPI host and key
RAPIDAPI_KEY = "11e3fc3ad2msh56c305395769159p144f8ejsn846975f0e54d"
RAPIDAPI_HOST = "api-football-v1.p.rapidapi.com"

# Function to fetch player data for a given fixture ID
def get_fixture_players(fixture_id):
    url = f"https://api-football-v1.p.rapidapi.com/v3/fixtures/players"
    querystring = {"fixture": fixture_id}
    
    headers = {
        "x-rapidapi-host": RAPIDAPI_HOST,
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    
    response = requests.get(url, headers=headers, params=querystring)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data for fixture ID {fixture_id}: {response.status_code}")
        return None

# Initialize the final list to store all players' stats from all fixtures
all_players_stats = []

# Maximum API calls per minute
MAX_CALLS_PER_MINUTE = 5
SLEEP_TIME = 60 / MAX_CALLS_PER_MINUTE  # Time in seconds between each call

# Loop through fixture IDs and fetch the data
for idx, fixture_id in enumerate(fixture_ids):
    print(f"Fetching data for fixture ID: {fixture_id}")
    
    player_data = get_fixture_players(fixture_id)
    
    # If player data is successfully fetched
    if player_data:
        for team_data in player_data['response']:  # Iterate through both teams
            team = team_data.get('team', {})
            players_list = team_data.get('players', [])
            
            # Extract team data
            team_info = {f'team_{key}': value for key, value in team.items()}
            
            # Extract player and stats data
            for player_data in players_list:
                player_info = player_data.get('player', {})
                statistics = player_data.get('statistics', [])
                
                # Initialize the player dictionary to hold player info + team info + fixture_id
                player_stats = {'fixture_id': fixture_id}  # Add fixture_id here
                
                # Add team info to player stats
                player_stats.update(team_info)
                
                # Add player info
                for key, value in player_info.items():
                    player_stats[f'player_{key}'] = value
                
                # Add statistics (assuming it's a list of dictionaries)
                for stat in statistics:
                    for key, value in stat.items():
                        # If the value is a dictionary (nested stats), we need to flatten it
                        if isinstance(value, dict):
                            for sub_key, sub_value in value.items():
                                # Add the nested dictionary values to player_stats with a flattened key
                                player_stats[f'stat_{key}_{sub_key}'] = sub_value
                        else:
                            # If it's not a dictionary, add it directly
                            player_stats[f'stat_{key}'] = value
                
                # Append this player's stats to the final all_players_stats list
                all_players_stats.append(player_stats)
    
    # Sleep after each call to respect the rate limit (15 calls per minute)
    if (idx + 1) % MAX_CALLS_PER_MINUTE == 0:
        print(f"Pausing for {SLEEP_TIME} seconds to respect rate limit...")
        time.sleep(SLEEP_TIME)

# Convert the collected data into a DataFrame
players_df = pd.DataFrame(all_players_stats)

# Show the DataFrame
print(players_df)

# Optionally, save the DataFrame to a CSV file for later use
players_df.to_csv('euro_players_fixtures_stats.csv', index=False)
