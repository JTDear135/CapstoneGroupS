import requests

# Client ID and Secret for NotAM API
CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET = 'CLIENT_SECRET'

TOKEN_URL = 'https://external-api.faa.gov/notamapi/v1/notams' # What value should this be?

data = {
    'grant type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET
}

# Make the token request

response = requests.post(TOKEN_URL + '/token', data=data)

# Check if response was successful

if response.status_code == 200:
    # Extract the access token from the response JSON
    token_data = response.json()
    access_token = token_data['access_token']
    print("Access token retrieved successfully!")
else:
    print(f"Error fetching access token. Status code: {response.status_code}")
    print(f"Response: {response.text}")
