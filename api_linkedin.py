from flask import Blueprint, redirect, request, session, jsonify
import secrets
import requests

linkedin_bp = Blueprint("linkedin_bp", __name__)

LINKEDIN_CLIENT_ID = "77s4r41rne0e9i"
LINKEDIN_CLIENT_SECRET = "WPL_AP1.gsDI2ADDszrGUGAx.yviatA=="
LINKEDIN_REDIRECT_URI = "http://127.0.0.1:5000/auth/linkedin/callback"

@linkedin_bp.route("/auth/linkedin")
def linkedin_auth():
    """
    Step 1: Redirect to LinkedIn's OAuth 2.0 authorization endpoint,
    requesting the openid, profile, and email scopes.
    """
    state = secrets.token_hex(16)
    session["linkedin_oauth_state"] = state

    authorization_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={LINKEDIN_REDIRECT_URI}"
        # Request OIDC scopes: openid profile email
        "&scope=openid%20profile%20email"
        f"&state={state}"
    )

    return redirect(authorization_url)


@linkedin_bp.route("/auth/linkedin/callback")
def linkedin_callback():
    """
    Step 2: LinkedIn redirects here with ?code=...&state=...
    We verify the state, exchange the code for an access token,
    then call /v2/userinfo for user profile data.
    """
    code = request.args.get("code")
    returned_state = request.args.get("state")

    # Retrieve and pop the saved state token from session
    saved_state = session.pop("linkedin_oauth_state", None)

    # Verify that the returned state matches our saved state (CSRF check)
    if not returned_state or not saved_state or returned_state != saved_state:
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

    token_response = requests.post(token_url, data=token_data, timeout=10)
    if token_response.status_code != 200:
        return f"Failed to get access token: {token_response.text}", 400

    token_json = token_response.json()
    access_token = token_json.get("access_token")
    if not access_token:
        return "No access token received from LinkedIn", 400

    userinfo_url = "https://api.linkedin.com/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=headers, timeout=10)

    if userinfo_response.status_code != 200:
        return f"Failed to fetch userinfo: {userinfo_response.text}", 400

    userinfo_data = userinfo_response.json()

    # Extract some common fields
    sub = userinfo_data.get("sub")
    email = userinfo_data.get("email")
    name = userinfo_data.get("name")
    given_name = userinfo_data.get("given_name")
    family_name = userinfo_data.get("family_name")

    session["linkedin_user"] = {
        "sub": sub,
        "email": email,
        "name": name,
        "given_name": given_name,
        "family_name": family_name
    }

    return jsonify({
        "access_token": access_token,
        "userinfo_data": userinfo_data
    })
