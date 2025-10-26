"""
BC Bulletin Board Backend (Flask)
A Flask server to manage and display campus events.
"""
#imports statements for functionality
import json
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

#configuration for server
PORT = 8000
DATA_FILE = "events.json"
UPLOAD_DIR = "uploads"

#create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

#initialize Flask app
app = Flask(__name__)

#provide explannation 
CORS(app)

#helper functions -
def get_events():
    #load events from JSON file 
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        return [] #return empty list if file doesn't exist
    
    #filter out past events using try and except statements
    now = datetime.now()
    current_events = []
    
    for event in events:
        try:
            event_dt = datetime.fromisoformat(event['event_date'].replace('Z', '+00:00'))

            if event_dt > now:
                current_events.append(event)
        except Exception:
            #if date parsing fails, keep the event
            current_events.append(event)
    
    return current_events

def save_event(event):
    #saving event data to a JSON file
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []
    
    events.append(event)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=2)

#api endpoints 

@app.route("/", methods=['GET'])
def root():
    #shows current version for user
    return {"message": "EagleBoard", "version": "1.0.0"}


@app.route("/events", methods=['GET'])
def get_all_events():
    events = get_events()
    return jsonify(events)


@app.route("/events", methods=['POST'])
def create_event():
    #requesting necessary information for an event (title,description,date, and location)
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')
    
    #validate required fields
    if not title or not description or not event_date or not location:
        return jsonify({"error": "All fields are required"}), 400
    
    #validate that event date is not in the past
    try:
        # Handle both Z and +00:00 timezone formats
        if event_date.endswith('Z'):
            event_dt = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
        else:
            event_dt = datetime.fromisoformat(event_date)
        
        # Make both datetimes timezone-aware for comparison
        from datetime import timezone
        now = datetime.now(timezone.utc)
        
        if event_dt <= now:
            return jsonify({"error": "Event date must be in the future"}), 400
    except Exception as e:
        return jsonify({"error": f"Invalid date format: {str(e)}"}), 400
    
    #creating a unique upload for the folder to avoid overwrites
    poster_url = None
    if 'poster' in request.files:
        poster_file = request.files['poster']
        if poster_file.filename:
            #use a secure filename to prevent path traversal issues
            filename = secure_filename(poster_file.filename)
            #create a unique filename to avoid overwrites
            unique_filename = f"{uuid.uuid4()}_{filename}"
            upload_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            #save the file
            poster_file.save(upload_path)
        
            #this URL must match the static file serving endpoint
            poster_url = f"/uploads/{unique_filename}"

    #create new event as a dictionary
    event = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "event_date": event_date,
        "location": location,
        "poster_url": poster_url,
        "created_at": datetime.now().isoformat()
    }
    
    save_event(event)
    
    #return the created event with a 201 status code (means its good)
    return jsonify(event), 201

@app.route('/uploads/<filename>')
#uploading file from current directory, not anywhere else
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

#server startup (replaces main())
if __name__ == "__main__":
    """Start the server"""
    print(f"EagleBoard server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    #running the server
    app.run(host="0.0.0.0", port=PORT, debug=False)