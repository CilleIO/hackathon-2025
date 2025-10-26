import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import EventModal from './EventModal';

// Event data structure
interface Event {
  id: string;
  title: string;
  description: string;
  event_date: string;
  location: string;
  poster_url: string | null;
  created_at: string;
}

const API_URL = 'http://localhost:8000';

function App() {
  // State management
  const [events, setEvents] = useState<Event[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Fetch events from backend API
  const fetchEvents = async () => {
    try {
      const response = await axios.get<Event[]>(`${API_URL}/events`);
      // Sort events by date, soonest first
      const sortedEvents = response.data.sort((a, b) => new Date(a.event_date).getTime() - new Date(b.event_date).getTime());
      setEvents(sortedEvents);
    } catch (error) {
      console.error("Failed to fetch events:", error);
    }
  };

  // Load events on component mount
  useEffect(() => {
    fetchEvents();
  }, []);

  return (
    <div className="app">
      {/* Header with title and add event button */}
      <header className="header">
        <h1>EagleBoard</h1>
        <button className="add-event-btn" onClick={() => setIsModalOpen(true)}>
          Add Event
        </button>
      </header>
      
      {/* Main content area */}
      <main className="billboard">
        {events.length === 0 ? (
          // Empty state when no events
          <div className="no-events">
            <h2>Welcome to EagleBoard!</h2>
            <p>Click "Add Event" to get started.</p>
          </div>
        ) : (
          // Event grid display
          <div className="event-grid">
            {events.map(event => (
              <div key={event.id} className="event-card">
                {/* Optional poster image */}
                {event.poster_url && <img src={`${API_URL}${event.poster_url}`} alt={`${event.title} poster`} className="event-poster" />}
                <h2>{event.title}</h2>
                <p className="event-date">{new Date(event.event_date).toLocaleString()}</p>
                <p className="event-location">{event.location}</p>
                <p className="event-description">{event.description}</p>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Event creation modal */}
      <EventModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onEventAdded={fetchEvents} />
  </div>
  );
}

export default App;