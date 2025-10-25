#!/usr/bin/env python3
"""
Simple BC Bulletin Board Backend
A basic Python server that stores events in a JSON file
"""

import json
import os
import uuid
import shutil
from datetime import datetime
from typing import Optional

import uvicorn
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# --- Configuration ---
PORT = 8000
DATA_FILE = "events.json"
UPLOAD_DIR = "uploads"

# --- App Setup ---
# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize FastAPI app
app = FastAPI()

# --- CORS Middleware (Replaces do_OPTIONS) ---
# This handles all CORS preflight requests automatically
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# --- Static File Server (Replaces GET /uploads/...) ---
# This serves all files in the UPLOAD_DIR directory under the /uploads path
app.mount(f"/{UPLOAD_DIR}", StaticFiles(directory=UPLOAD_DIR), name="uploads")


# --- Helper Functions (Moved from class) ---
def get_events():
    """Load events from JSON file and filter out past events"""
    try:
        with open(DATA_FILE, 'r') as f:
            events = json.load(f)
    except FileNotFoundError:
        return []
    
    # Filter out past events
    now = datetime.now()
    current_events = []
    
    for event in events:
        try:
            # Assuming event_date is ISO format, make it timezone-aware for comparison
            event_dt = datetime.fromisoformat(event['event_date'].replace('Z', '+00:00'))
            # Make 'now' aware if event_dt is aware
            if event_dt.tzinfo:
                now = datetime.now(event_dt.tzinfo)
                
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
    except FileNotFoundError:
        events = []
    
    events.append(event)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(events, f, indent=2)

# --- API Endpoints (Replaces do_GET and do_POST) ---

@app.get("/")
def read_root():
    """Handle GET requests for /"""
    return {"message": "BC Digital Bulletin Board", "version": "1.0.0"}


@app.get("/events")
def read_events():
    """Handle GET requests for /events"""
    events = get_events()
    return events


@app.post("/events", status_code=201)
async def create_event(
    # FastAPI replaces cgi.FieldStorage.
    # It uses type hints to parse the form.
    title: str = Form(),
    description: str = Form(),
    event_date: str = Form(),
    location: str = Form(),
    poster: Optional[UploadFile] = File(None)
):
    """
    Handle POST requests for /events.
    FastAPI automatically validates required fields.
    If 'title', 'description', etc., are missing,
    it will return a 422 Unprocessable Entity error.
    """
    
    poster_url = None
    if poster and poster.filename:
        # Create a unique path to avoid overwriting files
        # A simple way for a hackathon is to use the original filename
        # In production, you'd want to sanitize this or use a UUID
        filename = poster.filename
        upload_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save the file
        try:
            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(poster.file, buffer)
        except Exception as e:
            # Handle file save error
            raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
        finally:
            poster.file.close()
        
        # This URL must match the StaticFiles mount path
        poster_url = f"/{UPLOAD_DIR}/{filename}"

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
    
    # Return the created event (FastAPI handles JSON conversion)
    return event


# --- Server Startup (Replaces main()) ---
if __name__ == "__main__":
    """Start the server"""
    print(f"BC Bulletin Board Server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    # uvicorn.run() replaces HTTPServer
    # "fastapi_backend:app" refers to the 'app' object in the file 'fastapi_backend.py'
    # Set reload=True for auto-restarting the server on code changes
    uvicorn.run("simple_backend:app", host="localhost", port=PORT, reload=True)