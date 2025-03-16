import requests

NEW_API_KEY ="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"
NEW_URL = "https://openrouter.ai/api/v1/chat/completions"

def init_deepseek_api():
    """
    Initialize the DeepSeek API.
    This function doesn't need to take any arguments since the API key is already defined globally.
    """
    print("DeepSeek API initialized with API key:", NEW_API_KEY)

def recommender_careerpath(user_data):
    # Get user data from front end
    headers = {
        "Authorization": f"Bearer {NEW_API_KEY}",
        "Content-Type": "application/json"
    }

    # Construct the prompt for deepseek 
    prompt = f"""
        Based on the following user data, recommend a career pathway:
        - Education: {user_data.get('education')}
        - Job History: {user_data.get('job_history')}
        - Skills: {user_data.get('skills')}
        - Interests: {user_data.get('interests')}
    """

    # Prepare the request payload
    payload = {
        "model": "deepseek/deepseek-chat:free",  # Replace with the correct model name
        "messages": [
            {"role": "system", "content": "You are a career advisor."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(NEW_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json().get("choices", [])[0].get("message", {}).get("content", "No recommendation available.")
    except requests.exceptions.RequestException as e:
        print(f"DeepSeek API Error: {e}")
        return "Failed to fetch career recommendation."

