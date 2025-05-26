import { useState } from 'react';
import './App.css';

function App() {
  const [idea, setIdea] = useState('');
  const [evaluation, setEvaluation] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:5000/api/evaluate-startup-idea', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ idea }),
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

  return (
    <div className="App">
      <header className="App-header">
        <h1>Startup Idea Evaluator</h1>
        <p className="subtitle">Get AI-powered feedback on your startup idea</p>
        
        <form onSubmit={handleSubmit} className="idea-form">
          <textarea
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            placeholder="Describe your startup idea here..."
            required
            className="idea-input"
          />
          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Evaluating...' : 'Evaluate Idea'}
          </button>
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
