# from flask import Flask, render_template, request
# from azure.data.tables import TableServiceClient
# import os
# from dotenv import load_dotenv
# import pandas as pd

# # Load environment variables from .env file
# load_dotenv()

# # Azure connection string
# connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# # Table names
# euro_table_name = "euroPlayerStats"
# laliga_table_name = "laligaPlayers"
# epl_table_name = "eplPlayers"

# # Initialize Table Service Client
# table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)

# # Table Clients
# euro_table_client = table_service_client.get_table_client(table_name=euro_table_name)
# laliga_table_client = table_service_client.get_table_client(table_name=laliga_table_name)
# epl_table_client = table_service_client.get_table_client(table_name=epl_table_name)

# # Load Euro players fixtures stats from CSV
# euro_fixtures_stats = pd.read_csv('euro_players_fixtures_stats.csv')

# app = Flask(__name__)

# # Columns to fetch
# columns_to_fetch = [
#     "name", "games_appearences", "games_minutes", 
#     "games_position", "games_rating", "goals_assists", 
#     "goals_total", "passes_accuracy", "team_name","id"
# ]

# def fetch_player_data(table_client, player_id, columns):
#     """Fetch specific columns of a player."""
#     try:
#         player_id_int = int(player_id)
#         filter_query = f"id eq {player_id_int}"
#         entities = table_client.query_entities(query_filter=filter_query, select=columns)
        
#         for entity in entities:
#             return entity
#         return None
#     except Exception as e:
#         print(f"Error fetching data for player ID {player_id}: {e}")
#         return None

# def fetch_team_players(table_client, team_name, columns):
#     """Fetch specific columns of players from a team."""
#     filter_query = f"team_name eq '{team_name}'"
#     entities = table_client.query_entities(query_filter=filter_query, select=columns)
#     return [entity for entity in entities]

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     player_data = None
#     if request.method == 'POST':
#         search_type = request.form.get('search_type')
        
#         if search_type == 'player_id':
#             player_id = request.form.get('player_id')
#             player_data = {
#                 "euro": [fetch_player_data(euro_table_client, player_id, columns_to_fetch)],
#                 "laliga": [fetch_player_data(laliga_table_client, player_id, columns_to_fetch)],
#                 "epl": [fetch_player_data(epl_table_client, player_id, columns_to_fetch)]
#             }
        
#         elif search_type == 'team_name':
#             team_name = request.form.get('team_name')
            
#             # Fetch players from Euro table
#             euro_players = fetch_team_players(euro_table_client, team_name, columns_to_fetch)
            
#             # Extract player IDs
#             player_ids = [player['id'] for player in euro_players if 'id' in player]
            
#             # Fetch players from La Liga and EPL tables whose IDs are in player_ids
#             laliga_players = [player for player_id in player_ids if (player := fetch_player_data(laliga_table_client, player_id, columns_to_fetch)) is not None]
#             epl_players = [player for player_id in player_ids if (player := fetch_player_data(epl_table_client, player_id, columns_to_fetch)) is not None]
            
#             player_data = {
#                 "euro": euro_players,
#                 "laliga": laliga_players,
#                 "epl": epl_players
#             }

#     return render_template('index.html', player_data=player_data)

# @app.route('/player/<player_id>', methods=['GET'])
# def player_details(player_id):
#     """Fetch and display player fixture stats from the CSV."""
#     player_fixtures = euro_fixtures_stats[euro_fixtures_stats['player_id'] == int(player_id)]
#     return render_template('player_details.html', player_fixtures=player_fixtures.to_dict(orient='records'))

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request
from azure.data.tables import TableServiceClient
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Azure connection string
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Table names
euro_table_name = "euroPlayerStats"
laliga_table_name = "laligaPlayers"
epl_table_name = "eplPlayers"
seriaa_table_name = "seriaAPlayerStats"  # New Seria A table

# Initialize Table Service Client
table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)

# Table Clients
euro_table_client = table_service_client.get_table_client(table_name=euro_table_name)
laliga_table_client = table_service_client.get_table_client(table_name=laliga_table_name)
epl_table_client = table_service_client.get_table_client(table_name=epl_table_name)
seriaa_table_client = table_service_client.get_table_client(table_name=seriaa_table_name)  # Seria A table client

# Load Euro players fixtures stats from CSV
euro_fixtures_stats = pd.read_csv('euro_players_fixtures_stats.csv')

app = Flask(__name__)

# Columns to fetch
columns_to_fetch = [
    "name", "games_appearences", "games_minutes", 
    "games_position", "games_rating", "goals_assists", 
    "goals_total", "passes_accuracy", "team_name", "id"
]

def fetch_player_data(table_client, player_id, columns):
    """Fetch specific columns of a player."""
    try:
        player_id_int = int(player_id)
        filter_query = f"id eq {player_id_int}"
        entities = table_client.query_entities(query_filter=filter_query, select=columns)
        
        for entity in entities:
            return entity
        return None
    except Exception as e:
        print(f"Error fetching data for player ID {player_id}: {e}")
        return None

def fetch_team_players(table_client, team_name, columns):
    """Fetch specific columns of players from a team."""
    filter_query = f"team_name eq '{team_name}'"
    entities = table_client.query_entities(query_filter=filter_query, select=columns)
    return [entity for entity in entities]

@app.route('/', methods=['GET', 'POST'])
def home():
    player_data = None
    if request.method == 'POST':
        search_type = request.form.get('search_type')
        
        if search_type == 'player_id':
            player_id = request.form.get('player_id')
            player_data = {
                "euro": [fetch_player_data(euro_table_client, player_id, columns_to_fetch)],
                "laliga": [fetch_player_data(laliga_table_client, player_id, columns_to_fetch)],
                "epl": [fetch_player_data(epl_table_client, player_id, columns_to_fetch)],
                "seriaa": [fetch_player_data(seriaa_table_client, player_id, columns_to_fetch)]  # Fetch from Seria A
            }
        
        elif search_type == 'team_name':
            team_name = request.form.get('team_name')
            
            # Fetch players from Euro table
            euro_players = fetch_team_players(euro_table_client, team_name, columns_to_fetch)
            
            # Extract player IDs
            player_ids = [player['id'] for player in euro_players if 'id' in player]
            
            # Fetch players from La Liga, EPL, and Seria A tables whose IDs are in player_ids
            laliga_players = [player for player_id in player_ids if (player := fetch_player_data(laliga_table_client, player_id, columns_to_fetch)) is not None]
            epl_players = [player for player_id in player_ids if (player := fetch_player_data(epl_table_client, player_id, columns_to_fetch)) is not None]
            seriaa_players = [player for player_id in player_ids if (player := fetch_player_data(seriaa_table_client, player_id, columns_to_fetch)) is not None]  # Fetch from Seria A
            
            player_data = {
                "euro": euro_players,
                "laliga": laliga_players,
                "epl": epl_players,
                "seriaa": seriaa_players  # Add Seria A players
            }

    return render_template('index.html', player_data=player_data)

@app.route('/player/<player_id>', methods=['GET'])
def player_details(player_id):
    """Fetch and display player fixture stats from the CSV."""
    player_fixtures = euro_fixtures_stats[euro_fixtures_stats['player_id'] == int(player_id)]
    return render_template('player_details.html', player_fixtures=player_fixtures.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
