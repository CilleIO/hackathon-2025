#!/usr/bin/env python3
"""
Simple BC Bulletin Board Backend
A basic Python server that stores events in a JSON file
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
import urllib.parse
import uuid

# Configuration
PORT = 8000
DATA_FILE = "events.json"
UPLOAD_DIR = "uploads"

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)

# For parsing multipart/form-data
import cgi


class BulletinHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "BC Digital Bulletin Board", "version": "1.0.0"}
            self.wfile.write(json.dumps(response).encode())
            
        elif self.path == "/events":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            events = self.get_events()
            self.wfile.write(json.dumps(events).encode())
            
        elif self.path.startswith("/uploads/"):
            # Serve uploaded files
            filename = self.path[9:]  # Remove "/uploads/" prefix
            filepath = os.path.join(UPLOAD_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == "/events":
            # Use cgi.FieldStorage to parse multipart/form-data
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })

            # Extract event data
            title = form.getvalue('title', '')
            description = form.getvalue('description', '')
            event_date = form.getvalue('event_date', '')
            location = form.getvalue('location', '')

            poster_url = None
            if 'poster' in form:
                poster_item = form['poster']
                if poster_item.filename:
                    # Sanitize filename
                    sanitized_filename = os.path.basename(poster_item.filename)
                    # Create a unique filename to avoid overwrites
                    unique_filename = f"{uuid.uuid4()}_{sanitized_filename}"
                    filepath = os.path.join(UPLOAD_DIR, unique_filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(poster_item.file.read())
                    
                    poster_url = f"/uploads/{unique_filename}"

            if not all([title, description, event_date, location]):
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                response = {"error": "Missing required fields"}
                self.wfile.write(json.dumps(response).encode())
                return
            
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
            self.save_event(event)
            
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(event).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_events(self):
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
                event_date = datetime.fromisoformat(event['event_date'].replace('Z', '+00:00'))
                if event_date > now:
                    current_events.append(event)
            except:
                # If date parsing fails, keep the event
                current_events.append(event)
        
        return current_events
    
    def save_event(self, event):
        """Save event to JSON file"""
        try:
            with open(DATA_FILE, 'r') as f:
                events = json.load(f)
        except FileNotFoundError:
            events = []
        
        events.append(event)
        
        with open(DATA_FILE, 'w') as f:
            json.dump(events, f, indent=2)

def main():
    """Start the server"""
    server = HTTPServer(('localhost', PORT), BulletinHandler)
    print(f"BC Bulletin Board Server running on http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()

if __name__ == "__main__":
    main()
