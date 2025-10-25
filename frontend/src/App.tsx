import React from 'react';
import './App.css';

function App() {
  return (
    <div className="app">
      <header className="header">
        <h1>🏛️ BC Digital Bulletin Board</h1>
        <button className="add-event-btn">
          + Add Event
        </button>
      </header>
      
      <main className="billboard">
        <div className="no-events">
          <h2>Welcome to BC Digital Bulletin Board!</h2>
          <p>Click "Add Event" to get started.</p>
        </div>
      </main>
    </div>
  );
}

export default App;