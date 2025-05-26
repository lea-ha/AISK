from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from dotenv import load_dotenv
from ai_service import AIService

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


ai_service = AIService()

@app.route('/api/health', methods=['GET'])
def health():
    logger.info("Health endpoint called...")
    return jsonify({"status": "ok"}), 200

@app.route('/api/evaluate-startup-idea', methods=['POST'])
def evaluate_startup_idea():
    logger.info("Evaluate startup idea endpoint called...")
    data = request.json
    idea = data.get('idea')
    if not idea:
        return jsonify({"error": "Idea is required"}), 400
    
    result = ai_service.evaluate_startup_idea(idea)
    logger.info(f"Evaluation result: {result}")
    return jsonify(result), 200

if __name__ == '__main__':
    load_dotenv()
    app.run(host='0.0.0.0', port=5000, debug=True)

