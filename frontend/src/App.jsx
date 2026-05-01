import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const handlePlayMusic = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setMessage({ text: 'Please enter a music request.', type: 'error' });
      return;
    }

    setIsLoading(true);
    setMessage({ text: '', type: '' });

    try {
      const response = await axios.post('http://localhost:5000/api/play-music', { query });
      
      if (response.status === 200) {
        setMessage({ 
          text: `Playing: ${response.data.keywords} on YouTube! 🎵`, 
          type: 'success' 
        });
      }
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setMessage({ 
          text: 'DECLINED: Not a music request. Try asking for a song!', 
          type: 'error' 
        });
      } else {
        setMessage({ 
          text: 'An error occurred. Make sure the backend and browser automation are running.', 
          type: 'error' 
        });
      }
    } finally {
      setIsLoading(false);
    }
  };

  const triggerAutoVibe = async () => {
    const autoQuery = "Pick the absolute best song or playlist that matches my current weather, day, and time!";
    setQuery(autoQuery);
    setIsLoading(true);
    setMessage({ text: '', type: '' });

    try {
      const response = await axios.post('http://localhost:5000/api/play-music', { query: autoQuery });
      
      if (response.status === 200) {
        setMessage({ 
          text: `Playing: ${response.data.keywords} on YouTube! 🎵`, 
          type: 'success' 
        });
      }
    } catch (error) {
      setMessage({ 
        text: 'An error occurred while fetching your auto vibe.', 
        type: 'error' 
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <div className="bg-blobs">
        <div className="blob1"></div>
        <div className="blob2"></div>
      </div>
      
      <div className="app-container">
        <div className="player-card">
          <div className="header">
            <h1>AI Music Player</h1>
            <p>Ask for any song, artist, or playlist</p>
          </div>

          <form onSubmit={handlePlayMusic}>
            <div className="form-group">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="e.g., Play some Coldplay..."
                className="search-input"
                disabled={isLoading}
              />
            </div>

            <div style={{ display: 'flex', gap: '16px' }}>
              <button
                type="submit"
                disabled={isLoading || !query.trim()}
                className="play-button"
                style={{ flex: 1 }}
              >
                <span>
                  {isLoading ? 'Wait...' : 'Play Music 🎧'}
                </span>
              </button>

              <button
                type="button"
                onClick={triggerAutoVibe}
                disabled={isLoading}
                className="play-button"
                style={{ flex: 1, background: 'linear-gradient(135deg, #10b981 0%, #0284c7 100%)' }}
              >
                <span>
                  {isLoading ? 'Wait...' : 'Auto Vibe 🌤️'}
                </span>
              </button>
            </div>
          </form>

          {message.text && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
