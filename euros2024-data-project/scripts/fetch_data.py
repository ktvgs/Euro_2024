import requests
import json
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Define your API endpoint and headers
API_URL = 'https://api-football-v1.p.rapidapi.com/v3/fixtures?league=4&season=2024'
HEADERS = {'x-rapidapi-host': 'api-football-v1.p.rapidapi.com','x-rapidapi-key':'11e3fc3ad2msh56c305395769159p144f8ejsn846975f0e54d'}

# Fetch data from the API
response = requests.get(API_URL, headers=HEADERS)
data = response.json()

# Save data to a JSON file locally
with open('matches.json', 'w') as json_file:
    json.dump(data, json_file)

# Azure Blob Storage configuration
connect_str = 'DefaultEndpointsProtocol=https;AccountName=eurodataktvgs;AccountKey=KV69H4kTv+OnWf/x2oaJMTK3UqfRqvV+b5JdnuOyTcEnXEBAvJoPAVj7J5DomQC5diVU6VeatW0a+AStuCq3jg==;EndpointSuffix=core.windows.net'
container_name = 'match-fixtures'

# Create a blob service client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
container_client = blob_service_client.get_container_client(container_name)

# Upload JSON file to Azure Blob Storage
blob_client = container_client.get_blob_client('matches.json')
with open('matches.json', 'rb') as data_file:
    blob_client.upload_blob(data_file, overwrite=True)

print('Data fetched and uploaded to Azure Blob Storage successfully.')
