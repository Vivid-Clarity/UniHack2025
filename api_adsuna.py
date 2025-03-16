import requests

# Replace with your Adzuna API credentials
APP_ID = "34642a3c"
APP_KEY = "aaac4ecbe98be4b09854f874c7bb57c1"

def search_jobs(search_query="", location="Australia", results_per_page=10, page=1):
    """
    Search for jobs using the Adzuna API.
    """
    url = "https://api.adzuna.com/v1/api/jobs/au/search"  # au is the country code for the australia
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": search_query,  # Job title or keyword
        "where": location,     # Location
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        # print(response)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []  # Fallback if API fails