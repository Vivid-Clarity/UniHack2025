from flask import Blueprint, jsonify, request

# Create a Blueprint for the events API
events_api_bp = Blueprint('events_api', __name__)

# Full Extended Event Data (20 Events)
events = [
    {
        "id": 1,
        "badge": "Fully booked",
        "type": "Networking",
        "title": "Tech Networking Night",
        "date": "March 25, 2025 | 6:00 PM",
        "location": "Melbourne, AU",
        "organizer": "Tech Corp",
        "description": "Join us for an evening of networking with top tech professionals.",
        "tags": ["Tech", "Networking", "Career Growth"],
        "posted": "Posted 3 days ago",
    },
    {
        "id": 2,
        "badge": "Upcoming",
        "type": "Workshop",
        "title": "AI Career Workshop",
        "date": "May 10, 2025 | 10:00 AM",
        "location": "Online",
        "organizer": "AI Academy",
        "description": "Learn how to kickstart your career in AI with hands-on workshops and expert guidance.",
        "tags": ["AI", "Workshop", "Career Growth"],
        "posted": "Posted 5 days ago",
    },
    {
        "id": 3,
        "badge": "Upcoming",
        "type": "Conference",
        "title": "Future of Web Development",
        "date": "April 15, 2025 | 9:00 AM",
        "location": "Melbourne, AU",
        "organizer": "Web Dev Summit",
        "description": "Explore the future of web development with industry leaders.",
        "tags": ["Web Development", "Conference", "Technology"],
        "posted": "Posted 2 days ago"
    },
    {
        "id": 4,
        "badge": "Upcoming",
        "type": "Hackathon",
        "title": "Global AI Hackathon",
        "date": "April 2, 2025 | 8:00 AM",
        "location": "Remote",
        "organizer": "AI Hackers United",
        "description": "Compete in a global AI hackathon, solve real-world problems, and win exciting prizes!",
        "tags": ["AI", "Hackathon", "Coding"],
        "posted": "Posted 7 days ago"
    },
    {
        "id": 5,
        "badge": "Upcoming",
        "type": "Meetup",
        "title": "Startup Founders Meetup",
        "date": "May 8, 2025 | 5:30 PM",
        "location": "Melbourne, AU",
        "organizer": "Startup Hub",
        "description": "Connect with fellow startup founders and network with investors.",
        "tags": ["Startups", "Networking", "Entrepreneurship"],
        "posted": "Posted 1 day ago"
    },
    {
        "id": 6,
        "badge": "Upcoming",
        "type": "Workshop",
        "title": "Blockchain Bootcamp",
        "date": "June 1, 2025 | 9:00 AM",
        "location": "Melbourne, Australia",
        "organizer": "Blockchain Academy",
        "description": "Master the fundamentals of blockchain technology and smart contracts.",
        "tags": ["Blockchain", "Workshop", "Crypto"],
        "posted": "Posted 2 days ago"
    },
    {
        "id": 7,
        "badge": "Upcoming",
        "type": "Webinar",
        "title": "Cybersecurity in 2025",
        "date": "June 5, 2025 | 2:00 PM",
        "location": "Online",
        "organizer": "Cyber Experts",
        "description": "A discussion on cybersecurity threats and best practices.",
        "tags": ["Cybersecurity", "Webinar", "Tech"],
        "posted": "Posted 6 days ago"
    },
    {
        "id": 8,
        "badge": "Upcoming",
        "type": "Conference",
        "title": "Data Science Summit",
        "date": "July 10, 2025 | 10:00 AM",
        "location": "Melbourne, AU",
        "organizer": "Big Data Institute",
        "description": "Explore the latest trends in machine learning and data science.",
        "tags": ["Data Science", "Conference", "AI"],
        "posted": "Posted 4 days ago"
    },
    {
        "id": 9,
        "badge": "Upcoming",
        "type": "Hackathon",
        "title": "Fintech Innovation Challenge",
        "date": "August 20, 2025 | 9:00 AM",
        "location": "AU",
        "organizer": "Fintech Labs",
        "description": "Solve real-world financial problems in this fintech hackathon.",
        "tags": ["Fintech", "Hackathon", "Startups"],
        "posted": "Posted 8 days ago"
    },
    {
        "id": 10,
        "badge": "Upcoming",
        "type": "Meetup",
        "title": "Women in Tech Meetup",
        "date": "September 5, 2025 | 6:30 PM",
        "location": "New York, NY",
        "organizer": "Women Who Code",
        "description": "A gathering of women in tech to share experiences and career insights.",
        "tags": ["Networking", "Women in Tech", "Meetup"],
        "posted": "Posted 10 days ago"
    },
    {
        "id": 11,
        "badge": "Upcoming",
        "type": "Conference",
        "title": "Quantum Computing Conference",
        "date": "November 2, 2025 | 10:00 AM",
        "location": "Sydney, Australia",
        "organizer": "Quantum Tech",
        "description": "Discover breakthroughs in quantum computing.",
        "tags": ["Quantum Computing", "Tech", "Conference"],
        "posted": "Posted 12 days ago"
    },
    {
        "id": 12,
        "badge": "Upcoming",
        "type": "Workshop",
        "title": "UX/UI Design Sprint",
        "date": "October 15, 2025 | 9:30 AM",
        "location": "San Francisco, CA",
        "organizer": "Design Labs",
        "description": "A hands-on UX/UI design workshop.",
        "tags": ["Design", "Workshop", "UX/UI"],
        "posted": "Posted 15 days ago"
    },
    {
        "id": 13,
        "badge": "Upcoming",
        "type": "Workshop",
        "title": "Python for Data Science",
        "date": "October 20, 2025 | 1:00 PM",
        "location": "Online",
        "organizer": "DataHub Academy",
        "description": "A Python programming workshop focused on data analysis.",
        "tags": ["Python", "Workshop", "Data Science"],
        "posted": "Posted 15 days ago"
    },
    {
        "id": 14,
        "badge": "Upcoming",
        "type": "Networking",
        "title": "AI & Robotics Networking Night",
        "date": "November 15, 2025 | 7:00 PM",
        "location": "Melbourne, Australia",
        "organizer": "AI Robotics Alliance",
        "description": "An exclusive networking event for AI and robotics professionals.",
        "tags": ["AI", "Robotics", "Networking"],
        "posted": "Posted 5 days ago"
    },
    {
        "id": 15,
        "badge": "Upcoming",
        "type": "Workshop",
        "title": "Deep Learning Masterclass",
        "date": "December 2, 2025 | 9:00 AM",
        "location": "Toronto, Canada",
        "organizer": "AI Mastery",
        "description": "A deep dive into neural networks and AI model training.",
        "tags": ["AI", "Deep Learning", "Workshop"],
        "posted": "Posted 7 days ago"
    },
    {
        "id": 16,
        "badge": "Upcoming",
        "type": "Conference",
        "title": "5G & IoT World Summit",
        "date": "January 20, 2026 | 10:00 AM",
        "location": "Dubai, UAE",
        "organizer": "Global Tech Forum",
        "description": "Exploring the future of 5G and the Internet of Things.",
        "tags": ["5G", "IoT", "Conference"],
        "posted": "Posted 10 days ago"
    },
    {
        "id": 17,
        "badge": "Upcoming",
        "type": "Hackathon",
        "title": "Autonomous Vehicle Coding Challenge",
        "date": "February 5, 2026 | 8:00 AM",
        "location": "Detroit, MI",
        "organizer": "AutoTech Innovators",
        "description": "Develop smart driving algorithms for self-driving cars.",
        "tags": ["AI", "Autonomous Vehicles", "Hackathon"],
        "posted": "Posted 12 days ago"
    },
    {
        "id": 18,
        "badge": "Upcoming",
        "type": "Meetup",
        "title": "Tech Leaders Roundtable",
        "date": "March 12, 2026 | 6:00 PM",
        "location": "London, UK",
        "organizer": "Global Tech Leaders",
        "description": "An exclusive meetup for CTOs, CIOs, and tech innovators.",
        "tags": ["Tech Leadership", "Networking", "Meetup"],
        "posted": "Posted 14 days ago"
    },
    {
        "id": 19,
        "badge": "Upcoming",
        "type": "Webinar",
        "title": "The Future of Cloud Computing",
        "date": "April 5, 2026 | 4:00 PM",
        "location": "Online",
        "organizer": "Cloud Innovations",
        "description": "A webinar on emerging trends in cloud infrastructure.",
        "tags": ["Cloud Computing", "Webinar", "Tech"],
        "posted": "Posted 16 days ago"
    },
    {
        "id": 20,
        "badge": "Upcoming",
        "type": "Conference",
        "title": "Space Tech Summit 2026",
        "date": "May 8, 2026 | 10:00 AM",
        "location": "Houston, TX",
        "organizer": "NASA Tech Group",
        "description": "A conference on the latest advancements in space technology.",
        "tags": ["Space Tech", "Aerospace", "Conference"],
        "posted": "Posted 18 days ago"
    }

]

# Route to get all events
@events_api_bp.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events)

# Route to search for events
@events_api_bp.route('/api/events/search', methods=['GET'])
def search_events():
    query = request.args.get("query", "").lower()
    location = request.args.get("location", "").lower()

    filtered_events = [
        event for event in events
        if (query in event["title"].lower() or query in event["organizer"].lower() or any(query in tag.lower() for tag in event["tags"]))
        and (location in event["location"].lower())
    ]

    return jsonify(filtered_events)
