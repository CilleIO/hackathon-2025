# BC Digital Bulletin Board MVP

A simple digital bulletin board for Boston College campus events. This MVP allows users to add events with custom posters and automatically removes past events.

## Features

- ✅ **Simple Event Creation**: Click "Add Event" button to create new events
- ✅ **Custom Posters**: Upload images for event flyers/posters
- ✅ **Event Details**: Title, description, date/time, and location
- ✅ **Automatic Cleanup**: Past events are automatically filtered out
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **BC Branding**: Maroon and gold color scheme

## Project Structure

```
hackathon/
├── backend/
│   ├── main.py              # FastAPI backend
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── src/
│   │   ├── App.tsx         # Main React component
│   │   ├── App.css         # Styling
│   │   └── index.tsx       # React entry point
│   └── package.json        # Node.js dependencies
└── README.md              # This file
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend server:
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

   The app will be available at `http://localhost:3000`

## How to Use

1. **View Events**: The main page displays all upcoming events in a grid layout
2. **Add Event**: Click the "Add Event" button in the top-right corner
3. **Fill Form**: Complete the event form with:
   - Event title (required)
   - Description (required)
   - Date and time (required)
   - Location (required)
   - Poster image (optional)
4. **Submit**: Click "Add Event" to post to the bulletin board
5. **Automatic Cleanup**: Past events are automatically removed from the display

## API Endpoints

- `GET /events` - Retrieve all upcoming events
- `POST /events` - Create a new event
- `DELETE /events/{id}` - Delete an event
- `GET /` - API health check

## Technical Details

### Backend
- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **File Storage**: Local file system for uploaded images
- **CORS**: Configured for React development server

### Frontend
- **Framework**: React with TypeScript
- **Styling**: Custom CSS with BC branding
- **HTTP Client**: Axios for API calls
- **Date Handling**: date-fns library

### Database Schema
- **Events Table**:
  - `id` (Primary Key)
  - `title` (String)
  - `description` (Text)
  - `event_date` (DateTime)
  - `location` (String)
  - `poster_url` (String, optional)
  - `created_at` (DateTime)

## Development Checklist

### ✅ Completed Features
- [x] FastAPI backend with SQLite database
- [x] React frontend with TypeScript
- [x] Event creation form with validation
- [x] Image upload for event posters
- [x] Event display in grid layout
- [x] Automatic filtering of past events
- [x] Responsive design for mobile/desktop
- [x] BC-themed styling (maroon/gold)
- [x] File upload handling
- [x] Error handling and loading states

### 🔄 Future Enhancements
- [ ] User authentication system
- [ ] Event categories and filtering
- [ ] Search functionality
- [ ] Event approval workflow
- [ ] Push notifications
- [ ] Integration with BC systems (Agora Portal)
- [ ] Event analytics and insights
- [ ] Mobile app development
- [ ] Social sharing features
- [ ] Event RSVP functionality

## Troubleshooting

### Common Issues

1. **Backend not starting**: Ensure all dependencies are installed and port 8000 is available
2. **Frontend not connecting**: Check that the backend is running on port 8000
3. **Image upload issues**: Ensure the `uploads` directory exists and has proper permissions
4. **CORS errors**: Verify the backend CORS settings include `http://localhost:3000`

### File Permissions
Make sure the `uploads` directory has write permissions:
```bash
chmod 755 uploads/
```

## Contributing

This is an MVP for a hackathon project. For production use, consider:
- Adding proper authentication
- Implementing input validation
- Adding unit tests
- Setting up proper deployment
- Adding monitoring and logging
- Implementing proper error handling

## License

This project is created for educational purposes as part of a hackathon.
