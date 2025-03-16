from flask import Flask, render_template, jsonify, request
import api_adsuna
from events_api import events_api_bp # Import Blueprint
from api_linkedin import linkedin_bp
<<<<<<< HEAD
from api_deepseek import init_deepseek_api, recommender_careerpath  # Import DeepSeek API methods

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'

# Initialize DeepSeek API
init_deepseek_api()
=======

app = Flask(__name__)
app.secret_key = 'some_random_secret_key'
>>>>>>> 38fe280bcd4ccd94a8bcb1c59eca8154c294d54b

# Register the Blueprint
app.register_blueprint(events_api_bp)
app.register_blueprint(linkedin_bp)

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

# adsuna api
@app.route("/api/searchJobs")
def search_jobs_route():
    # Get search query and location from the request
    search_query = request.args.get("query", "")
    location = request.args.get("location", "")

    # Fetch jobs from the Adzuna API
    jobs = api_adsuna.search_jobs(search_query, location)
    # print(jobs)  # Log the jobs fetched from the API
    return jsonify(jobs)


# DeepSeek API route
@app.route("/api/recommendCareer", methods=["POST"])
def recommend_career():
    # Get user data from the front end
    user_data = request.json

    # Validate user data
    if not user_data:
        return jsonify({"error": "No data provided"}), 400

    # Call the DeepSeek API to get a career recommendation
    recommendation = recommender_careerpath(user_data)

    # Return the recommendation as JSON
    return jsonify({"recommendation": recommendation})


if __name__ == "__main__":
    app.run(debug=True)