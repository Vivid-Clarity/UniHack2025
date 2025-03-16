from flask import Flask, render_template, jsonify, request
import api_adsuna
from events_api import events_api_bp # Import Blueprint

app = Flask(__name__)

#Register the Blueprint
app.register_blueprint(events_api_bp)

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

if __name__ == "__main__":
    app.run(debug=True)