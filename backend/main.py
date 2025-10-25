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

#Configuration for server
PORT = 8000
DATA_FILE = "events.json"
UPLOAD_DIR = "uploads"

#Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

#Initialize Flask app
app = Flask(__name__)

#PROVIDE EXPLANNATION 
CORS(app)

#Helper Functions -
def get_events():
    #Load events from JSON file 
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        return [] # Return empty list if file doesn't exist
    
    #Filter out past events using try and except statements
    now = datetime.now()
    current_events = []
    
    for event in events:
        try:
            event_dt = datetime.fromisoformat(event['event_date'].replace('Z', '+00:00'))

            if event_dt > now:
                current_events.append(event)
        except Exception:
            #If date parsing fails, keep the event
            current_events.append(event)
    
    return current_events

def save_event(event):
    #Saving event to a Jason file
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []
    
    events.append(event)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=2)

#API Endpoints 

@app.get("/")
def root():
    #Shows current version for user
    return {"message": "EagleBoard", "version": "1.0.0"}


@app.get("/events")
def get_all_events():
    events = get_events()
    return jsonify(events)


@app.post("/events")
def create_event():
    #Requesting necessary information for an event (title,description,date, and location)
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')
    
    #creating an unique upload for the folder 
    poster_url = None
    if 'poster' in request.files:
        poster_file = request.files['poster']
        if poster_file.filename:
            #Use a secure filename to prevent path traversal issues
            filename = secure_filename(poster_file.filename)
            #Create a unique filename to avoid overwrites
            unique_filename = f"{uuid.uuid4()}_{filename}"
            upload_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            #Save the file
            poster_file.save(upload_path)
        
            #This URL must match the static file serving endpoint
            poster_url = f"/uploads/{unique_filename}"

    #Create new event as a dictionary
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
    
    #Return the created event with a 201 status code (means its good)
    return jsonify(event), 201

@app.route('/uploads/<filename>')
#Uploading file from current directory, not anywhere else
def uploaded_file(filename):
    return send_from_directory(UPLOAD_DIR, filename)

#Server Startup (Replaces main())
if __name__ == "__main__":
    """Start the server"""
    print(f"EagleBoard server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    #Running the server
    app.run(host="0.0.0.0", port=PORT, debug=False)