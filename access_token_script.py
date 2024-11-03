from dotenv import load_dotenv, set_key
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Retrieve API credentials from environment variables
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
CODE = os.getenv('CODE')
REDIRECT_URI = "https://127.0.0.2"

# URL for the token request
url = 'https://api.upstox.com/v2/login/authorization/token'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = {
    'code': CODE,
    'client_id': API_KEY,
    'client_secret': API_SECRET,
    'redirect_uri': REDIRECT_URI,
    'grant_type': 'authorization_code',
}

# Function to save the access token to the .env file
def save_access_token(token: str):
    # Open the .env file in append mode and write the token
    with open('.env', 'a') as env_file:
        env_file.write(f"ACCESS_TOKEN={token}\n")
    print("Access token saved to .env file.")

# Make the POST request to get the access token
try:
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()  # Raise an error for bad responses
    resp = response.json()

    # Check if the access token is in the response
    if 'access_token' in resp:
        access_token = resp['access_token']
        save_access_token(access_token)  # Save the access token to .env
    else:
        print("Access token not found in the response.")

except requests.RequestException as e:
    print(f"API request failed: {e}")
except KeyError as e:
    print(f"Missing expected data in response: {e}")
