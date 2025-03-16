from flask import Blueprint, redirect, request, session, jsonify
import secrets
import requests

linkedin_bp = Blueprint("linkedin_bp", __name__)

# LinkedIn OAuth Credentials
LINKEDIN_CLIENT_ID = "77s4r41rne0e9i"
LINKEDIN_CLIENT_SECRET = "WPL_AP1.gsDI2ADDszrGUGAx.yviatA=="
LINKEDIN_REDIRECT_URI= "http://127.0.0.1:5000/auth/linkedin/callback"

@linkedin_bp.route("/auth/linkedin")
def linkedin_auth():
    """
    Step 1: Redirect the user to LinkedIn's authorization page.
    """
    state = secrets.token_hex(16)
    session["linkedin_oauth_state"] = state

    authorization_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={LINKEDIN_REDIRECT_URI}"
        "&scope=openid%20profile%20email"  # << New scopes
        f"&state={state}"
    )

    return redirect(authorization_url)


@linkedin_bp.route("/auth/linkedin/callback")
def linkedin_callback():
    """
    Step 2: LinkedIn redirects back to this route with a `code`
    which we exchange for an access token.
    """
    # Retrieve the code and state from the incoming request
    code = request.args.get("code")
    state = request.args.get("state")

    # Retrieve and pop the saved state from the session
    saved_state = session.pop("linkedin_oauth_state", None)

    # Verify the state to protect against CSRF
    if not state or not saved_state or state != saved_state:
        return "Invalid state parameter", 400

    # Exchange the authorization code for an access token
    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": LINKEDIN_REDIRECT_URI,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    response = requests.post(token_url, data=token_data, timeout=10)
    if response.status_code != 200:
        return f"Failed to get access token: {response.text}", 400

    token_json = response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return "No access token received from LinkedIn", 400

    # 1. Basic profile
    profile_url = "https://api.linkedin.com/v2/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_response = requests.get(profile_url, headers=headers, timeout=10)
    profile_data = profile_response.json()

    # 2. Email
    email_url = "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))"
    email_response = requests.get(email_url, headers=headers, timeout=10)
    email_data = email_response.json()

    # Extract user data
    first_name = profile_data.get("localizedFirstName", "")
    last_name = profile_data.get("localizedLastName", "")
    email_address = None

    elements = email_data.get("elements", [])
    if elements and "handle~" in elements[0]:
        email_address = elements[0]["handle~"].get("emailAddress")

    # Store or process user data as needed
    session["linkedin_user"] = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email_address,
    }

    return jsonify({
        "access_token": access_token,
        "profile_data": profile_data,
        "email_data": email_data
    })
