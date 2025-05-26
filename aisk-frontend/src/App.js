import { useState } from 'react';
import './App.css';

// Use different URLs for development vs production
const getServerUrl = () => {
  const hostname = window.location.hostname;
  if (hostname.includes(".replit.dev") || hostname.includes(".repl.co")) {
    const baseUrl = `${window.location.protocol}//${hostname}`;
    return `${baseUrl}:5000/api`;
  }

  return "http://localhost:5000/api";
};

const serverUrl = getServerUrl();

function App() {
  const [idea, setIdea] = useState('');
  const [location, setLocation] = useState('Remote/Online');
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(serverUrl + '/evaluate-startup-idea', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea, location }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to evaluate idea');
      }
      
      const data = await response.json();
      setEvaluation(data);
    } catch (err) {
      setError('Failed to evaluate your idea. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setIdea('');
    setLocation('Remote/Online');
    setEvaluation(null);
    setError(null);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Startup Idea Evaluator</h1>
        <p className="subtitle">Get AI-powered feedback on your startup idea</p>
        
        <form onSubmit={handleSubmit} className="idea-form">
          <div className="form-group">
            <label htmlFor="location">Location:</label>
            <input
              type="text"
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Enter city, country, or 'Remote/Online'"
              className="location-input"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="idea">Your Startup Idea:</label>
            <textarea
              id="idea"
              value={idea}
              onChange={(e) => setIdea(e.target.value)}
              placeholder="Describe your startup idea here..."
              required
              className="idea-input"
            />
          </div>
          
          <div className="button-group">
            <button type="submit" disabled={loading} className="submit-button">
              {loading ? 'Evaluating...' : 'Evaluate Idea'}
            </button>
            <button 
              type="button" 
              onClick={handleReset} 
              className="reset-button"
              disabled={loading}
            >
              Reset
            </button>
          </div>
        </form>

        {error && <div className="error-message">{error}</div>}

        {evaluation && (
          <div className={`evaluation-result ${evaluation.verdict.toLowerCase().replace(' ', '-')}`}>
            <h2>Evaluation Result</h2>
            <div className="verdict">
              <span className="verdict-label">Verdict:</span>
              <span className="verdict-value">{evaluation.verdict}</span>
            </div>
            
            <div className="explanation">
              <h3>Key Points:</h3>
              <ul>
                {evaluation.explanation.map((point, index) => (
                  <li key={index}>{point}</li>
                ))}
              </ul>
            </div>
            
            <div className="location-impact">
              <h3>Location Impact:</h3>
              <p>{evaluation.location_impact}</p>
            </div>
            
            <div className="improvement">
              <h3>Improvement Suggestion:</h3>
              <p>{evaluation.improvement}</p>
            </div>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
