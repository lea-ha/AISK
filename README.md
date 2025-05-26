# Startup Idea Evaluator

An AI-powered tool that evaluates startup ideas and provides detailed feedback. The application uses GPT-3.5 to analyze startup ideas based on various criteria including problem clarity, market opportunity, differentiation, and feasibility.

## Features

- AI-powered startup idea evaluation
- Location-based context analysis
- Detailed feedback with key points and improvement suggestions
- Modern, responsive UI
- Real-time evaluation results

## Prerequisites

- Python 3.7+
- Node.js 14+
- npm (comes with Node.js)
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up the backend:
```bash
cd aisk-backend
pip install -r requirements.txt
```

3. Create a `.env` file in the `aisk-backend` directory:
```
OPENAI_API_KEY=your_openai_api_key_here
```

4. Set up the frontend:
```bash
cd aisk-frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd aisk-backend
python api.py
```
The backend server will run on http://localhost:5000

2. In a new terminal, start the frontend:
```bash
cd aisk-frontend
npm start
```
The frontend will run on http://localhost:3000

3. Open your browser and navigate to http://localhost:3000

## Usage

1. Enter your location context (city, country, or "Remote/Online")
2. Describe your startup idea in detail
3. Click "Evaluate Idea" to get AI-powered feedback
4. Review the evaluation results:
   - Overall verdict
   - Key points
   - Improvement suggestions
5. Use the "Reset" button to start a new evaluation

## Project Structure

```
.
├── aisk-backend/
│   ├── api.py           # Flask backend server
│   ├── ai_service.py    # OpenAI integration
│   └── requirements.txt # Python dependencies
│
└── aisk-frontend/
    ├── src/
    │   ├── App.js       # Main React component
    │   └── App.css      # Styles
    └── package.json     # Node.js dependencies
```

## Technologies Used

- Backend:
  - Python
  - Flask
  - OpenAI GPT-3.5
  - Flask-CORS

- Frontend:
  - React
  - Modern CSS
  - Fetch API

## Notes

- Make sure both the backend and frontend servers are running simultaneously
- The backend server must be running on port 5000
- The frontend will automatically connect to the backend
- Keep your OpenAI API key secure and never commit it to version control 