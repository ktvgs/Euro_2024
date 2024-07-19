import os
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient
from azure.data.tables import TableServiceClient, TableEntity
from azure.core.exceptions import ResourceExistsError

# Azure Blob Storage configuration
blob_connection_string = 'DefaultEndpointsProtocol=https;AccountName=eurodataktvgs;AccountKey=KV69H4kTv+OnWf/x2oaJMTK3UqfRqvV+b5JdnuOyTcEnXEBAvJoPAVj7J5DomQC5diVU6VeatW0a+AStuCq3jg==;EndpointSuffix=core.windows.net'
blob_container_name = 'match-fixtures'
blob_name = 'matches.json'

# Azure Table Storage configuration
table_connection_string = 'DefaultEndpointsProtocol=https;AccountName=eurodataktvgs;AccountKey=KV69H4kTv+OnWf/x2oaJMTK3UqfRqvV+b5JdnuOyTcEnXEBAvJoPAVj7J5DomQC5diVU6VeatW0a+AStuCq3jg==;EndpointSuffix=core.windows.net'
table_name = 'matchfixtures1'

# Access JSON data from Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=blob_name)

# Download the JSON file
json_data = blob_client.download_blob().readall()
data = json.loads(json_data)

# Extract relevant fields and create DataFrame
response = data['response']

# Extract fields
extracted_data = []
for match in response:
    match_id = match['fixture']['id']
    date = match['fixture']['date']
    home_team = match['teams']['home']['name']
    away_team = match['teams']['away']['name']
    round_name = match['league']['round']
    home_team_score = match['goals']['home']
    away_team_score = match['goals']['away']
    final_score = f"{home_team_score} - {away_team_score}"
    winner_team = match['teams']['home']['name'] if match['teams']['home']['winner'] else match['teams']['away']['name']
    duration = match['fixture']['status']['elapsed']
    
    extracted_data.append({
        'match_id': match_id,
        'date': date,
        'home_team': home_team,
        'away_team': away_team,
        'round': round_name,
        'home_team_score': home_team_score,
        'away_team_score': away_team_score,
        'final_score': final_score,
        'winner_team': winner_team,
        'duration': duration
    })

# Create DataFrame
df = pd.DataFrame(extracted_data)

# Store DataFrame in Azure Table Storage
table_service_client = TableServiceClient.from_connection_string(table_connection_string)

try:
    table_service_client.create_table_if_not_exists(table_name)
except ResourceExistsError:
    pass

table_client = table_service_client.get_table_client(table_name)

# Convert DataFrame to a list of dictionaries and insert into Azure Table Storage
for index, row in df.iterrows():
    entity = TableEntity()
    entity['PartitionKey'] = 'match'
    entity['RowKey'] = str(row['match_id'])
    entity['Date'] = row['date']
    entity['HomeTeam'] = row['home_team']
    entity['AwayTeam'] = row['away_team']
    entity['Round'] = row['round']
    entity['HomeTeamScore'] = row['home_team_score']
    entity['AwayTeamScore'] = row['away_team_score']
    entity['FinalScore'] = row['final_score']
    entity['WinnerTeam'] = row['winner_team']
    entity['Duration'] = row['duration']
    table_client.create_entity(entity=entity)

print('Data stored in Azure Table Storage successfully.')
