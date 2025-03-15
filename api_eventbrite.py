from datetime import datetime, timedelta, timezone
import requests

API_KEY = "NMQD62E6FYOPTRMD7ULR"
AUTHENTICATION_URL = "https://www.eventbriteapi.com/v3"

# Endpoint to fetch events (replace with your organization ID or user ID)
ENDPOINT = '/events/search/'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {API_KEY}',
}


# Parameters for the request
params = {
    'q': "CyberSecuirty",  # Search for events with the keyword "Valentine's"
    'location.address': 'Clayton, Australia',  # Set location to Clayton, Australia
    'expand': 'venue',  # Include venue details
}

# Make the GET request
response = requests.get(f'{AUTHENTICATION_URL}{ENDPOINT}', headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:

    # Parse the JSON response
    data = response.json()
    print("Full API Response:", data)  # Debug: Print the full response
    print("Pagination:", data.get('pagination'))  # Debug: Print pagination info

    events = data.get('events', [])
    
    # Print event details
    if events:
        for event in events:
            event_name = event['name']['text']
            event_url = event['url']
            start_time = event['start']['local']
            venue = event.get('venue', {}).get('name', 'Venue not specified')
            
            print(f"Event Name: {event_name}")
            print(f"Event URL: {event_url}")
            print(f"Start Time: {start_time}")
            print(f"Venue: {venue}")
            print('---')
    else:
        print("No events found for the specified search criteria.")
else:
    print(f"Failed to fetch events. Status code: {response.status_code}")
    print(f"Error: {response.text}")
