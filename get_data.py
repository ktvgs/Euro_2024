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

def fetch_player_data(table_client, player_id):
    """Fetch all columns of a player from the specified table using the id column."""
    try:
        # Convert player_id to integer if necessary
        player_id_int = int(player_id)
        
        # Use a filter query to search for the player by the 'id' column
        filter_query = f"id eq {player_id_int}"
        entities = table_client.query_entities(query_filter=filter_query)
        
        # Return the first matching entity (assuming 'id' is unique)
        for entity in entities:
            return entity
        return None
    except Exception as e:
        print(f"Error fetching data for player ID {player_id}: {e}")
        return None

def main():
    player_id_str = input("Enter Player ID: ")
    
    # Convert input to integer if necessary
    try:
        player_id = int(player_id_str)
    except ValueError:
        print("Invalid input: Player ID should be an integer.")
        return
    
    # Fetch data from euroPlayers table
    euro_player_data = fetch_player_data(euro_table_client, player_id)
    
    # Fetch data from laligaPlayers table
    laliga_player_data = fetch_player_data(laliga_table_client, player_id)
    
    # Display results
    if euro_player_data or laliga_player_data:
        print("Player Data:")
        
        if euro_player_data:
            print("\nEuro Players Data:")
            for key, value in euro_player_data.items():
                print(f"{key}: {value}")
        
        if laliga_player_data:
            print("\nLa Liga Players Data:")
            for key, value in laliga_player_data.items():
                print(f"{key}: {value}")
    else:
        print("No data found for the provided Player ID in both tables.")

if __name__ == "__main__":
    main()
