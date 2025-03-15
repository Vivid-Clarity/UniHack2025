import requests

# Replace with your API key
API_KEY = "your_api_key_here"

# API endpoint for job search
url = "https://www.themuse.com/api/public/jobs"

# Parameters for the request (e.g., search for remote Python jobs)
params = {
    "category": "Software Engineering",  # Optional: Filter by category
    "location": "Melbourne, Australia",                # Optional: Filter by location
    "page": 1                            # Optional: Pagination
}

# Headers with API key
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Make the request
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    jobs = response.json()
    for job in jobs["results"]:
        print(f"Job Title: {job['name']}")
        print(f"Company: {job['company']['name']}")
        print(f"Location: {job['locations'][0]['name']}")
        print(f"Link: {job['refs']['landing_page']}")
        print("-" * 40)
else:
    print(f"Error: {response.status_code} - {response.text}")