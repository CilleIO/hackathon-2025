#!/usr/bin/env python3
"""
BC Bulletin Board Backend

A FastAPI server to manage and display campus events.
"""

import json
import os
from datetime import datetime, timezone
import uuid
from typing import List, Optional, Dict

from fastapi import FastAPI, Form, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

# --- Configuration ---
DATA_FILE = "events.json"
UPLOAD_DIR = "uploads"

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="BC Digital Bulletin Board API",
    description="API for managing campus events.",
    version="1.1.0",
)

# --- CORS Middleware ---
# Allows the frontend (running on localhost:3000) to communicate with the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Data Validation ---
class Event(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    event_date: datetime
    location: str
    poster_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

# --- Helper Functions for Data Storage ---
def get_events() -> List[Event]:
    """Load events from JSON file and filter out past events."""
    try:
        with open(DATA_FILE, 'r') as f:
            events_data = json.load(f)
            events = [Event(**e) for e in events_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    # Filter out past events
    now = datetime.now(timezone.utc)
    current_events = [event for event in events if event.event_date > now]
    
    # Sort events by date
    current_events.sort(key=lambda x: x.event_date)
    
    return current_events

def save_event(event: Event):
    """Save a new event to the JSON file."""
    # Read existing events, excluding past ones
    events = get_events()
    events.append(event)
    
    # Convert list of Event objects to list of dicts for JSON serialization
    events_data = [e.model_dump(mode='json') for e in events]
    
    with open(DATA_FILE, 'w') as f:
        json.dump(events_data, f, indent=2)

# --- API Endpoints ---
@app.get("/", summary="API Health Check")
def health_check() -> Dict[str, str]:
    """Provides a simple health check for the API."""
    return {"message": "BC Digital Bulletin Board API is running", "version": "1.1.0"}

@app.get("/events", response_model=List[Event], summary="Get Upcoming Events")
def read_events():
    """Retrieve a list of all upcoming events, sorted by date."""
    return get_events()

@app.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED, summary="Create a New Event")
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    event_date: datetime = Form(...),
    location: str = Form(...),
    poster: Optional[UploadFile] = File(None)
):
    """
    Create a new event. Accepts form data, including an optional poster image.
    """
    poster_url = None
    if poster and poster.filename:
        # Sanitize filename to prevent security issues
        sanitized_filename = os.path.basename(poster.filename)
        # Create a unique filename to avoid overwrites
        unique_filename = f"{uuid.uuid4()}_{sanitized_filename}"
        filepath = os.path.join(UPLOAD_DIR, unique_filename)

        # Save the uploaded file
        with open(filepath, "wb") as buffer:
            buffer.write(await poster.read())

        poster_url = f"/uploads/{unique_filename}"

    new_event = Event(
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        poster_url=poster_url,
    )
    save_event(new_event)
    return new_event

@app.get("/uploads/{filename}", summary="Serve an Uploaded Poster")
async def get_upload(filename: str):
    """Serves an uploaded event poster from the `uploads` directory."""
    filepath = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(filepath)

if __name__ == "__main__":
    import uvicorn
    print("Starting BC Bulletin Board Server with FastAPI...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
