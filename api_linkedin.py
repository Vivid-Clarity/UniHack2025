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
    returned_state = request.args.get("state")

    saved_state = session.pop("linkedin_oauth_state", None)  # remove from session to prevent reuse


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

    # Call the OpenID Connect endpoint to get user info (OIDC profile + email)
    oidc_url = "https://api.linkedin.com/v2/oidcUserInfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    oidc_response = requests.get(oidc_url, headers=headers, timeout=10)

    if oidc_response.status_code != 200:
        return f"Failed to fetch userinfo: {oidc_response.text}", 400

    oidc_data = oidc_response.json()
    # Example fields: "sub", "email", "email_verified", "name", "given_name", "family_name", "picture", "locale", etc.

    # Extract some common fields
    sub = oidc_data.get("sub")
    email = oidc_data.get("email")
    email_verified = oidc_data.get("email_verified")
    full_name = oidc_data.get("name")
    given_name = oidc_data.get("given_name")
    family_name = oidc_data.get("family_name")

    # Store user data in session (or a database) for later use
    session["linkedin_user"] = {
        "sub": sub,
        "email": email,
        "email_verified": email_verified,
        "full_name": full_name,
        "given_name": given_name,
        "family_name": family_name
    }

    return jsonify({
        "access_token": access_token,
        "oidc_data": oidc_data,
    })
