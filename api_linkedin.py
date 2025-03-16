import authlib
from authlib.integrations.flask_client import OAuth
import os

# Initialize OAuth for LinkedIn
def init_linkedin_oauth(app):
    """
    Initialize LinkedIn OAuth and return the OAuth object.
    """
    oauth = OAuth(app)
    linkedin = oauth.register(
        name='linkedin',
        client_id=os.getenv('LINKEDIN_CLIENT_ID', '86gv9fugeofl1g'),  # Use environment variable or fallback
        client_secret=os.getenv('LINKEDIN_CLIENT_SECRET', 'WPL_AP1.nA0NRD4YAOkauuIf.7TEgcQ=='),  # Use environment variable or fallback
        authorize_url='https://www.linkedin.com/oauth/v2/authorization',
        authorize_params=None,
        access_token_url='https://www.linkedin.com/oauth/v2/accessToken',
        access_token_params=None,
        refresh_token_url=None,
        redirect_uri="http://localhost:5000/auth/linkedin/callback",
        client_kwargs={'scope': 'r_liteprofile r_emailaddress'},  # Requested scopes
    )
    return linkedin

def get_linkedin_profile(linkedin):
    """
    Fetch the LinkedIn profile of the authenticated user.
    """
    profile = linkedin.get('https://api.linkedin.com/v2/me')
    return profile.json()

def get_linkedin_email(linkedin):
    """
    Fetch the LinkedIn email of the authenticated user.
    """
    email = linkedin.get('https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))')
    return email.json()