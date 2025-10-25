# Simple BC Bulletin Board Backend

This is a very simple Python backend that a first-year programmer would write. No complex frameworks, just basic Python with file storage.

## Features

- ✅ **Simple HTTP Server** - Uses Python's built-in `http.server`
- ✅ **JSON File Storage** - Stores events in a simple JSON file
- ✅ **Automatic Cleanup** - Removes past events automatically
- ✅ **CORS Support** - Works with frontend
- ✅ **No Dependencies** - Only uses Python standard library

## How to Run

```bash
cd backend
python simple_backend.py
```

That's it! No virtual environment, no pip install, no complex setup.

## API Endpoints

- `GET /` - Health check
- `GET /events` - Get all upcoming events (automatically filters out past events)
- `POST /events` - Create new event

## How It Works

1. **Data Storage**: Events are stored in `events.json` file
2. **File Uploads**: Images are saved in `uploads/` directory
3. **Automatic Cleanup**: Past events are filtered out when you request the list
4. **Simple Logic**: Just reads/writes JSON files

## File Structure

```
backend/
├── simple_backend.py    # The server
├── events.json         # Event data (created automatically)
└── uploads/            # Image files (created automatically)
```

## Example Usage

### Create an event:

```bash
curl -X POST http://localhost:8000/events \
  -d "title=BC Basketball Game" \
  -d "description=Come watch BC vs Duke" \
  -d "event_date=2024-01-15T19:00:00" \
  -d "location=Conte Forum"
```

### Get all events:

```bash
curl http://localhost:8000/events
```

## Why This Approach?

- **No Dependencies**: Works with any Python installation
- **Easy to Understand**: First-year programmer can read and modify
- **Reliable**: No complex framework issues
- **Portable**: Just copy the file and run it anywhere
- **Debuggable**: Easy to see what's happening in the JSON file

This is perfect for a hackathon MVP!
