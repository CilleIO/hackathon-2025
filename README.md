# EagleBoard - BC Digital Bulletin Board

A digital bulletin board for Boston College campus events. Students can post events with custom flyers and the system prevents creating past events.

## What it does

- **Post Events**: Click "Add Event" to create campus event posts
- **Upload Flyers**: Add custom images for your event posters
- **Event Info**: Include title, description, date/time, and location
- **Past Event Prevention**: System blocks creation of events with past dates
- **Mobile Friendly**: Works on phones and computers
- **BC Colors**: Maroon and gold theme

## Project Structure

```
hackathon/
├── backend/
│   ├── main.py             # Flask backend server
│   ├── events.json         # Event data storage
│   ├── uploads/            # Image storage (ignored by git)
│   └── venv/               # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── App.css         # Styling
│   │   ├── EventModal.tsx  # Event creation form
│   │   └── index.tsx       # App entry point
│   └── package.json        # Dependencies
├── .gitignore              # Git ignore rules
└── README.md              # This file
```

## Quick Start

### Backend

1. Go to the backend folder:

   ```bash
   cd backend
   ```

2. Activate virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Start the server:
   ```bash
   python3 main.py
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
5. **Validation**: System prevents creating events with past dates

## API

- `GET /events` - Get all upcoming events
- `POST /events` - Create a new event
- `GET /` - Health check

## Tech Stack

### Backend

- **Language**: Python 3
- **Framework**: Flask with Flask-CORS
- **Storage**: JSON file for events, local files for images
- **Validation**: Prevents past event creation
- **File Upload**: Handles image uploads with unique filenames

### Frontend

- **Framework**: React with TypeScript
- **Styling**: Custom CSS with BC branding
- **HTTP**: Axios for API calls
- **Build**: Create React App
- **Modal**: Event creation form with validation

## What's Done

- [x] Flask backend with virtual environment
- [x] React frontend with event display
- [x] Event creation form with file upload
- [x] Image storage and display
- [x] Past event validation (prevents creation)
- [x] Form validation and error handling
- [x] Responsive design
- [x] BC maroon/gold styling
- [x] Modal close functionality
- [x] Git ignore for uploads

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

**Backend won't start**: Make sure port 8000 isn't already in use and virtual environment is activated
**Flask not found**: Run `source venv/bin/activate` in the backend directory
**Frontend won't connect**: Check that backend is running on port 8000  
**Images not showing**: Make sure the `uploads` folder exists
**Past event error**: System prevents creating events with past dates - use future dates only
**Modal won't close**: Try clicking outside the modal or the X button

## Notes

This is a hackathon MVP built for simplicity. For a real production app, you'd want to add proper authentication, input validation, tests, and better deployment setup.

Built for the BC community! 🦅
