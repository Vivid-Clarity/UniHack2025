import requests

API_KEY = "f7f914b9b885356c28807ced4a220e3af192f3b5470fe9ba608e352ba970ce7d"

url = "https://www.themuse.com/api/public/jobs"

def headers():
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    return headers

def getJobs(job_id):
    url = f"https://www.themuse.com/api/public/jobs/{job_id}"
    res = requests.get(url, headers=headers())
    return res