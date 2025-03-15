import requests

# Replace with your Adzuna API credentials
APP_ID = "your_app_id_here"
APP_KEY = "your_app_key_here"

def search_jobs(search_query="", location="", results_per_page=10, page=1):
    """
    Search for jobs using the Adzuna API.
    """
    url = "https://api.adzuna.com/v1/api/jobs/au/search/1"  # au is the country code for the australia
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": search_query,  # Job title or keyword
        "where": location,     # Location
        "page": page           # Pagination
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []  # Fallback if API fails