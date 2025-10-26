/**
 * EventModal Component
 * 
 * A React modal component for creating new campus events in the BC Digital Bulletin Board.
 * This component handles event creation, file uploads, and API integration.
 */

import React, { useState, FormEvent, useEffect } from 'react';
import axios from 'axios';
import './EventModal.css';

/**
 * Props interface for EventModal component
 * 
 * @interface EventModalProps
 * @property {boolean} isOpen 
 * @property {() => void} onClose 
 * @property {() => void} onEventAdded 
 */
interface EventModalProps {
  isOpen: boolean;
  onClose: () => void;
  onEventAdded: () => void;
}

// Backend API endpoint for event management
const API_URL = 'http://localhost:8000';

/**
 * EventModal Component
 * 
 * @param {EventModalProps} props - Component props
 * @returns {JSX.Element | null} Modal component or null if not open
 */
const EventModal: React.FC<EventModalProps> = ({ isOpen, onClose, onEventAdded }) => {
  // Form state management - each field has its own state
  const [title, setTitle] = useState('');           // Event title
  const [description, setDescription] = useState(''); // Event description
  const [eventDate, setEventDate] = useState('');   // Event date and time
  const [location, setLocation] = useState('');     // Event location
  const [poster, setPoster] = useState<File | null>(null); // Uploaded poster file
  const [error, setError] = useState('');            // Error message display
  const [isSubmitting, setIsSubmitting] = useState(false); // Loading state

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen) {
      setTitle('');
      setDescription('');
      setEventDate('');
      setLocation('');
      setPoster(null);
      setError('');
    }
  }, [isOpen]);

  // Early return if modal is not open - improves performance
  if (!isOpen) {
    return null;
  }

  /**
   * Handles file input changes for poster uploads
   * 
   * @param {React.ChangeEvent<HTMLInputElement>} e - File input change event
   */
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPoster(e.target.files[0]);
    }
  };

  /**
   * Handles form submission for event creation
   * @param {FormEvent} e - Form submission event
   */
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    
    // Required fields validation
    if (!title || !description || !eventDate || !location) {
      setError('All fields except poster are required.');
      return;
    }
    
    // Clear previous errors and set loading state
    setError('');
    setIsSubmitting(true);

    // Create FormData object for multipart form submission
    // This allows us to send both text data and file uploads
    const formData = new FormData();
    formData.append('title', title);
    formData.append('description', description);
    formData.append('event_date', new Date(eventDate).toISOString()); 
    formData.append('location', location);
    
    // Add poster file if one was selected
    if (poster) {
      formData.append('poster', poster);
    }

    try {
      // Send POST request to backend API
      await axios.post(`${API_URL}/events`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Required for file uploads
        },
      });
      
      // Success: refresh events list and close modal
      onEventAdded(); // Trigger parent component to refresh events
      
      // Reset form state
      setTitle('');
      setDescription('');
      setEventDate('');
      setLocation('');
      setPoster(null);
      setError('');
      
      onClose();     // Close the modal
    } catch (err: any) {
      // Error handling: log error and show specific message
      console.error('Failed to add event:', err);
      
      // Show specific error message from backend if available
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('Failed to submit event. Please try again.');
      }
    } finally {
      // Always reset loading state
      setIsSubmitting(false);
    }
  };

  
   //Render the modal component
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Modal header with title and close button */}
        <h2>Add New Event</h2>
        <button onClick={onClose} className="close-button">&times;</button>
        
        {/* Event creation form */}
        <form onSubmit={handleSubmit}>
          {}
          {error && <p className="error-message">{error}</p>}
          
          {/* Event title input */}
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input 
              id="title" 
              type="text" 
              value={title} 
              onChange={(e) => setTitle(e.target.value)} 
              required 
            />
          </div>
          
          {/* Event description textarea */}
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea 
              id="description" 
              value={description} 
              onChange={(e) => setDescription(e.target.value)} 
              required 
            />
          </div>
          
          {/* Event date and time input */}
          <div className="form-group">
            <label htmlFor="event_date">Date and Time</label>
            <input 
              id="event_date" 
              type="datetime-local" 
              value={eventDate} 
              onChange={(e) => setEventDate(e.target.value)} 
              required 
            />
          </div>
          
          {/* Event location input */}
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input 
              id="location" 
              type="text" 
              value={location} 
              onChange={(e) => setLocation(e.target.value)} 
              required 
            />
          </div>
          
          {/* Optional poster image upload */}
          <div className="form-group">
            <label htmlFor="poster">Poster Image</label>
            <input 
              id="poster" 
              type="file" 
              accept="image/*" 
              onChange={handleFileChange} 
            />
          </div>
          
          {/* Submit button with loading state */}
          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Submitting...' : 'Add Event'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default EventModal;