"""
This is the old job finder API I used
Problem is that we can only search for specific pre defined catagories,
limiting our web sites capalbilities

NOT IN USE IN FINAL PRODUCT
"""


import requests

API_KEY = "f7f914b9b885356c28807ced4a220e3af192f3b5470fe9ba608e352ba970ce7d"

def headers():
    return {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

def get_jobs(search_query="", location="", page=1):
    print("query = " + search_query)
    url = "https://www.themuse.com/api/public/jobs"
    params = {
        "page": page,
        "descending": "true"  # Sort by newest jobs first
    }

    # Add search query and location if provided
    if search_query:
        params["category"] = search_query
    if location:
        params["location"] = location

    res = requests.get(url, headers=headers())
    if res.status_code == 200:
        return res.json().get("results", [])
    else:
        return []