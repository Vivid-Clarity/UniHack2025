from flask import Flask, render_template

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)