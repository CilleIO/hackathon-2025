#!/usr/bin/env python3
"""
BC Bulletin Board Backend (Flask)
A simple Flask server to manage and display campus events.
"""

import json
import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# --- Configuration ---
PORT = 8000
DATA_FILE = "events.json"
UPLOAD_DIR = "uploads"

# --- App Setup ---
# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI app
app = Flask(__name__)

# --- CORS ---
CORS(app) # This will allow all origins

# --- Static File Server (Replaces GET /uploads/...) ---
# This serves all files in the UPLOAD_DIR directory under the /uploads path


# --- Helper Functions (Moved from class) ---
def get_events():
    """Load events from JSON file and filter out past events"""
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        return [] # Return empty list if file doesn't exist
    
    # Filter out past events
    now = datetime.now()
    current_events = []
    
    for event in events:
        try:
            # Assuming event_date is ISO format
            event_dt = datetime.fromisoformat(event['event_date'].replace('Z', '+00:00'))
            # Make 'now' aware if event_dt is aware
            if event_dt.tzinfo:
                now = datetime.now(event_dt.tzinfo) # Use timezone-aware comparison
                
            if event_dt > now:
                current_events.append(event)
        except Exception:
            # If date parsing fails, keep the event
            current_events.append(event)
    
    return current_events

def save_event(event):
    """Save event to JSON file"""
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        events = []
    
    events.append(event)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=2)

# --- API Endpoints (Replaces do_GET and do_POST) ---

@app.get("/")
def root():
    """Handle GET requests for /"""
    return {"message": "BC Digital Bulletin Board", "version": "1.0.0"}


@app.get("/events")
def get_all_events():
    """Handle GET requests for /events"""
    events = get_events()
    return jsonify(events)


@app.post("/events")
def create_event():
    """
    Handle POST requests for /events.
    """
    # Flask's 'request' object contains the form data
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')
    
    poster_url = None
    if 'poster' in request.files:
        poster_file = request.files['poster']
        if poster_file.filename:
            # Use a secure filename to prevent path traversal issues
            filename = secure_filename(poster_file.filename)
            # Create a unique filename to avoid overwrites
            unique_filename = f"{uuid.uuid4()}_{filename}"
            upload_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Save the file
            poster_file.save(upload_path)
        
            # This URL must match the static file serving endpoint
            poster_url = f"/uploads/{unique_filename}"

    # Create new event
    event = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "event_date": event_date,
        "location": location,
        "poster_url": poster_url,
        "created_at": datetime.now().isoformat()
    }
    
    # Save event
    save_event(event)
    
    # Return the created event with a 201 status code
    return jsonify(event), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serves uploaded files."""
    return send_from_directory(UPLOAD_DIR, filename)

# --- Server Startup (Replaces main()) ---
if __name__ == "__main__":
    """Start the server"""
    print(f"BC Bulletin Board Server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    # Use Flask's built-in server for development
    app.run(host="0.0.0.0", port=PORT, debug=False)