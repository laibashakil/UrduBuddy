from flask import Flask, request, jsonify
from flask_cors import CORS
from rag.rag_system import UrduRAG
import os

app = Flask(__name__)
CORS(app)

# Initialize RAG system
rag = UrduRAG("data/urdu_data.json")

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        response = rag.query(question)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 