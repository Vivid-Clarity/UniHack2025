from flask import Flask, render_template, jsonify, request, url_for, redirect, session
import api_adsuna
from events_api import events_api_bp # Import Blueprint
from api_linkedin import init_linkedin_oauth, get_linkedin_profile, get_linkedin_email  # Import LinkedIn API methods

app = Flask(__name__)

#Register the Blueprint
app.register_blueprint(events_api_bp)

# Initialize LinkedIn OAuth
linkedin = init_linkedin_oauth(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jobTracker")
def jobTracker():
    return render_template("job-tracker.html")

@app.route("/eventFinder")
def eventFinder():
    return render_template("event-finder.html")

@app.route("/careerRecommender")
def careerRecommender():
    return render_template("career-recommender.html")

@app.route("/resumeBuilder")
def resumeBuilder():
    return render_template("resume-builder.html")


#------------------------------------------------------
#API shii

# the muse api
@app.route("/api/searchJobs")
def search_jobs():
    #getting search and location form the request
    search_query = request.args.get("query", "")
    location = request.args.get("location", "")

    #getting the jobs from Muse API
    jobs = api_adsuna.get_jobs(search_query,location)
    print(jobs)
    return jsonify(jobs)

# adsuna api
@app.route("/api/searchJobs")
def search_jobs_route():
    # Get search query and location from the request
    search_query = request.args.get("query", "")
    location = request.args.get("location", "")

    # Fetch jobs from the Adzuna API
    jobs = api_adsuna.search_jobs(search_query, location)
    print(jobs)  # Log the jobs fetched from the API
    return jsonify(jobs)

# LinkedIn login route
@app.route('/login/linkedin')
def linkedin_login():
    redirect_uri = url_for('linkedin_callback', _external=True)
    return linkedin.authorize_redirect(redirect_uri)

# LinkedIn callback route
@app.route('/auth/linkedin/callback')
def linkedin_callback():
    token = linkedin.authorize_access_token()
    if not token:
        return "Failed to retrieve access token.", 400

    # Store the token in the session
    session['linkedin_token'] = token

    # Fetch user profile and email
    profile = get_linkedin_profile(linkedin)
    email = get_linkedin_email(linkedin)

    # Store user data in the session
    session['linkedin_profile'] = profile
    session['linkedin_email'] = email

    return redirect(url_for('profile'))

# Profile route
@app.route('/profile')
def profile():
    if 'linkedin_profile' not in session:
        return redirect(url_for('home'))

    profile = session['linkedin_profile']
    email = session['linkedin_email']

    return f"""
        <h1>LinkedIn Profile</h1>
        <p>Name: {profile.get('localizedFirstName')} {profile.get('localizedLastName')}</p>
        <p>Email: {email.get('elements')[0].get('handle~').get('emailAddress')}</p>
        <p>Profile ID: {profile.get('id')}</p>
        <a href="/logout">Logout</a>
    """

# Logout route
@app.route('/logout')
def logout():
    session.pop('linkedin_token', None)
    session.pop('linkedin_profile', None)
    session.pop('linkedin_email', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)