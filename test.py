import requests

API_KEY = "NMQD62E6FYOPTRMD7ULR"

url = "https://www.eventbriteapi.com/v3/events/search/"

params = {
    "q": "cyber security",  # Search query (e.g., "technology", "music", etc.)
    "location.address": "Glen Waverley",  # Location (optional)
    "sort_by": "date",  # Sort by date
    "token": API_KEY  # Your API key
}

response = requests.get(url, params=params)

if response.status_code == 200:
    events = response.json().get("events", [])
    for event in events:
        print(f"Event: {event['name']['text']}")
        print(f"Date: {event['start']['local']}")
        print(f"URL: {event['url']}")
        print("-" * 40)
else:
    print(f"Error: {response.status_code} - {response.text}")