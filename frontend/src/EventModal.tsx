import React, { useState, FormEvent } from 'react';
import axios from 'axios';
import './EventModal.css';

interface EventModalProps {
  isOpen: boolean;
  onClose: () => void;
  onEventAdded: () => void;
}

const API_URL = 'http://localhost:8000';

const EventModal: React.FC<EventModalProps> = ({ isOpen, onClose, onEventAdded }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [eventDate, setEventDate] = useState('');
  const [location, setLocation] = useState('');
  const [poster, setPoster] = useState<File | null>(null);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  if (!isOpen) {
    return null;
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPoster(e.target.files[0]);
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!title || !description || !eventDate || !location) {
      setError('All fields except poster are required.');
      return;
    }
    setError('');
    setIsSubmitting(true);

    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('event_date', new Date(eventDate).toISOString());
    formData.append('location', location);
    if (poster) {
      formData.append('poster', poster);
    }

    try {
      await axios.post(`${API_URL}/events`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      onEventAdded(); // Refresh events list
      onClose(); // Close modal
    } catch (err) {
      console.error('Failed to add event:', err);
      setError('Failed to submit event. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Add New Event</h2>
        <button onClick={onClose} className="close-button">&times;</button>
        <form onSubmit={handleSubmit}>
          {error && <p className="error-message">{error}</p>}
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input id="title" type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea id="description" value={description} onChange={(e) => setDescription(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="event_date">Date and Time</label>
            <input id="event_date" type="datetime-local" value={eventDate} onChange={(e) => setEventDate(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input id="location" type="text" value={location} onChange={(e) => setLocation(e.target.value)} required />
          </div>
          <div className="form-group">
            <label htmlFor="poster">Poster Image</label>
            <input id="poster" type="file" accept="image/*" onChange={handleFileChange} />
          </div>
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Submitting...' : 'Add Event'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EventModal;