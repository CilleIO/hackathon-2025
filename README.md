# EagleBoard - BC Digital Bulletin Board

A digital bulletin board for Boston College campus events. Students can post events with custom flyers and the system automatically removes outdated events.

## What it does

- **Post Events**: Click "Add Event" to create campus event posts
- **Upload Flyers**: Add custom images for your event posters
- **Event Info**: Include title, description, date/time, and location
- **Auto Cleanup**: Past events disappear automatically
- **Mobile Friendly**: Works on phones and computers
- **BC Colors**: Maroon and gold theme

## Project Structure

```
hackathon/
├── backend/
│   ├── simple_backend.py   # Python backend server
│   └── events.json         # Event data storage
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── App.css         # Styling
│   │   ├── EventModal.tsx  # Event creation form
│   │   └── index.tsx       # App entry point
│   └── package.json        # Dependencies
├── start.sh               # Quick start script
└── README.md              # This file
```

## Quick Start

The easiest way to get everything running:

```bash
./start.sh
```

This will start both the backend and frontend servers automatically.

## Manual Setup

### Backend

1. Go to the backend folder:

   ```bash
   cd backend
   ```

2. Run the server:
   ```bash
   python3 simple_backend.py
   ```

The backend runs on `http://localhost:8000`

### Frontend

1. Go to the frontend folder:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the app:
   ```bash
   npm start
   ```

The app opens at `http://localhost:3000`

## How it works

1. **View Events**: See all upcoming events on the main page
2. **Add Event**: Click "Add Event" button in the top-right
3. **Fill Out Form**: Enter event details and optionally upload a poster image
4. **Submit**: Click "Add Event" to post it to the board
5. **Auto Removal**: Events automatically disappear after their date passes

## API

- `GET /events` - Get all upcoming events
- `POST /events` - Create a new event
- `GET /` - Health check

## Tech Stack

### Backend

- **Language**: Python 3
- **Server**: Built-in http.server (no external dependencies)
- **Storage**: JSON file for events, local files for images
- **CORS**: Handles cross-origin requests

### Frontend

- **Framework**: React with TypeScript
- **Styling**: Custom CSS with BC branding
- **HTTP**: Axios for API calls
- **Build**: Create React App

## What's Done

- [x] Simple Python backend (no dependencies needed)
- [x] React frontend with event display
- [x] Event creation form with file upload
- [x] Image storage and display
- [x] Automatic past event removal
- [x] Responsive design
- [x] BC maroon/gold styling
- [x] Error handling
- [x] Loading states

## Future Ideas

- [ ] User accounts and login
- [ ] Event categories (academic, social, etc.)
- [ ] Search and filter events
- [ ] Event approval system
- [ ] Push notifications
- [ ] Integration with BC systems
- [ ] Event analytics
- [ ] Mobile app
- [ ] Social sharing
- [ ] RSVP functionality

## Common Issues

**Backend won't start**: Make sure port 8000 isn't already in use
**Frontend won't connect**: Check that backend is running on port 8000  
**Images not showing**: Make sure the `uploads` folder exists
**CORS errors**: Backend should handle this automatically

## Notes

This is a hackathon MVP built for simplicity. For a real production app, you'd want to add proper authentication, input validation, tests, and better deployment setup.

Built for the BC community! 🦅
