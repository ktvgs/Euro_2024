from flask import Flask, render_template, request
from azure.data.tables import TableServiceClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure connection string
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Table names
euro_table_name = "euroPlayers"
laliga_table_name = "laligaPlayers"

# Initialize Table Service Client
table_service_client = TableServiceClient.from_connection_string(conn_str=connection_string)

# Table Clients
euro_table_client = table_service_client.get_table_client(table_name=euro_table_name)
laliga_table_client = table_service_client.get_table_client(table_name=laliga_table_name)

app = Flask(__name__)

def fetch_player_data(table_client, player_id, column_name=None):
    """Fetch specific column data or all columns of a player."""
    try:
        player_id_int = int(player_id)
        filter_query = f"id eq {player_id_int}"
        select_columns = [column_name] if column_name else None
        entities = table_client.query_entities(query_filter=filter_query, select=select_columns)
        
        for entity in entities:
            return entity
        return None
    except Exception as e:
        print(f"Error fetching data for player ID {player_id}: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    player_data = None
    selected_column = None
    if request.method == 'POST':
        player_id = request.form.get('player_id')
        selected_column = request.form.get('column')
        
        euro_player_data = fetch_player_data(euro_table_client, player_id, selected_column)
        laliga_player_data = fetch_player_data(laliga_table_client, player_id, selected_column)
        
        player_data = {
            "euro": euro_player_data,
            "laliga": laliga_player_data
        }
        
    return render_template('index.html', player_data=player_data, selected_column=selected_column)

if __name__ == '__main__':
    app.run(debug=True)
