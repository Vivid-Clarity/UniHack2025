import requests

# Replace with your Adzuna API credentials
APP_ID = "34642a3c"  # Your actual App ID
APP_KEY = "aaac4ecbe98be4b09854f874c7bb57c1"  # Your actual App Key

def search_jobs(search_query="", location="Australia", results_per_page=10, page=1):
    """
    Search for jobs using the Adzuna API.
    """
    url = f"https://api.adzuna.com/v1/api/jobs/au/search"  # au is the country code for Australia
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": search_query,  # Job title or keyword
        "where": location,     # Location (default: "Australia")
    }

    try:
        print("Making API request with params:", params)  # Log the request parameters
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("results", [])
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")  # Log the API response for debugging
        return []  # Fallback if API fails

def main():
    # Test search parameters
    search_query = "software"  # Job title or keyword
    location = "Australia"     # Location

    # Fetch jobs from the Adzuna API
    jobs = search_jobs(search_query, location)

    # Print the jobs
    if jobs:
        print(f"Found {len(jobs)} jobs:")
        for job in jobs:
            print(f"\nJob Title: {job.get('title')}")
            print(f"Company: {job.get('company', {}).get('display_name')}")
            print(f"Location: {job.get('location', {}).get('display_name')}")
            print(f"Description: {job.get('description')}")
            print(f"URL: {job.get('redirect_url')}")
    else:
        print("No jobs found.")

if __name__ == "__main__":
    main()