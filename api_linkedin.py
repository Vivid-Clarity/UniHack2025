from flask import Blueprint, redirect, request, session, jsonify
import secrets
import requests

linkedin_bp = Blueprint("linkedin_bp", __name__)

<<<<<<< HEAD
# LinkedIn OAuth Credentials (Updated)
LINKEDIN_CLIENT_ID = "77s4r41rne0e9i"
LINKEDIN_CLIENT_SECRET = "WPL_AP1.gsDI2ADDszrGUGAx.yviatA=="
# LINKEDIN_REDIRECT_URI = "https://www.linkedin.com/developers/tools/oauth/redirect"

=======
# LinkedIn OAuth Credentials
LINKEDIN_CLIENT_ID = "77s4r41rne0e9i"
LINKEDIN_CLIENT_SECRET = "WPL_AP1.gsDI2ADDszrGUGAx.yviatA=="
>>>>>>> 38fe280bcd4ccd94a8bcb1c59eca8154c294d54b
LINKEDIN_REDIRECT_URI= "http://127.0.0.1:5000/auth/linkedin/callback"

@linkedin_bp.route("/auth/linkedin")
def linkedin_auth():
    """
    Step 1: Redirect the user to LinkedIn's authorization page.
    """
<<<<<<< HEAD
    # It's good practice to use a random state for CSRF protection
=======
>>>>>>> 38fe280bcd4ccd94a8bcb1c59eca8154c294d54b
    state = secrets.token_hex(16)
    session["linkedin_oauth_state"] = state

    authorization_url = (
        "https://www.linkedin.com/oauth/v2/authorization"
        "?response_type=code"
        f"&client_id={LINKEDIN_CLIENT_ID}"
        f"&redirect_uri={LINKEDIN_REDIRECT_URI}"
<<<<<<< HEAD
        "&scope=r_liteprofile%20r_emailaddress"
=======
        "&scope=openid%20profile%20email"  # << New scopes
>>>>>>> 38fe280bcd4ccd94a8bcb1c59eca8154c294d54b
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
<<<<<<< HEAD
    state = request.args.get("state")

    # Retrieve and pop the saved state from the session
    saved_state = session.pop("linkedin_oauth_state", None)
=======
    returned_state = request.args.get("state")

    saved_state = session.pop("linkedin_oauth_state", None)  # remove from session to prevent reuse

>>>>>>> 38fe280bcd4ccd94a8bcb1c59eca8154c294d54b

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

<<<<<<< HEAD
    # Use the token to get user info from LinkedIn
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
        "email": email_address
    }

    # For demo purposes, return JSON; in production, redirect or render a page
    return jsonify({
        "access_token": access_token,
        "profile_data": profile_data,
        "email_data": email_data
=======
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
>>>>>>> 38fe280bcd4ccd94a8bcb1c59eca8154c294d54b
    })
