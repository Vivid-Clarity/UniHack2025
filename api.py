import requests

API_KEY = "f7f914b9b885356c28807ced4a220e3af192f3b5470fe9ba608e352ba970ce7d"

# API endpoint for job search
url = "https://www.themuse.com/api/public/jobs"

# Headers with API key
def headers():
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

# Parameters for the request (e.g., search for remote Python jobs)
# all this is in the docs
# params = {
#     "category": "Software Engineering",  # Optional: Filter by category
#     "location": "Remote",                # Optional: Filter by location
#     "page": 1                            # Optional: Pagination
# }



# Make the request
# response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
# if response.status_code == 200:
#     jobs = response.json()
#     for job in jobs["results"]:
#         print(f"Job Title: {job['name']}")
#         print(f"Company: {job['company']['name']}")
#         print(f"Location: {job['locations'][0]['name']}")
#         print(f"Link: {job['refs']['landing_page']}")
#         print("-" * 40)
# else:
#     print(f"Error: {response.status_code} - {response.text}")

# print(response)