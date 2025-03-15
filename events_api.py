from flask import Blueprint, jsonify

# Create a Blueprint for the fake API
fake_api_bp = Blueprint('fake_api', __name__)

# Fake event data
events = [
    {
        "id": 1,
        "name": "Valentine's Day Dinner",
        "date": "2023-02-14T19:00:00",
        "location": "Romantic Restaurant, Clayton",
        "description": "Join us for a special Valentine's Day dinner with live music and a 3-course meal.",
        "organizer": "Clayton Events",
        "price": 50.0
    },
    {
        "id": 2,
        "name": "Tech Conference 2023",
        "date": "2023-03-15T09:00:00",
        "location": "Convention Center, Melbourne",
        "description": "A conference for tech enthusiasts featuring talks on AI, blockchain, and cloud computing.",
        "organizer": "Tech Innovators",
        "price": 100.0
    },
    {
        "id": 3,
        "name": "Art Exhibition Opening",
        "date": "2023-04-01T18:00:00",
        "location": "City Art Gallery, Melbourne",
        "description": "Experience the works of local artists at the opening night of our new exhibition.",
        "organizer": "Melbourne Art Society",
        "price": 20.0
    }
]

# Route to get all events
@fake_api_bp.route('/api/events', methods=['GET'])
def get_events():
    return jsonify(events)

# Route to get a specific event by ID
@fake_api_bp.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = next((event for event in events if event['id'] == event_id), None)
    if event:
        return jsonify(event)
    else:
        return jsonify({"error": "Event not found"}), 404