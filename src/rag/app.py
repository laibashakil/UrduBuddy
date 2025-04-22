from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from rag_system import UrduRAG
import os
import json

app = Flask(__name__)
CORS(app)

# Initialize RAG system with both stories and poems
rag = UrduRAG(
    stories_path="data/stories/urdu_stories.json",
    poems_path="data/poems"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({
                'status': 'error',
                'message': 'No question provided'
            }), 400
            
        response = rag.query(data['question'])
        return jsonify({
            'status': 'success',
            'data': response
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/stories/<path:story_id>')
def get_story(story_id):
    try:
        # Remove 'root/' prefix if present
        story_id = story_id.replace('root/', '')
        file_path = os.path.join('data', f'{story_id}.json')
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': f'Story not found: {story_id}'
            }), 404
            
        with open(file_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            return jsonify({
                'success': True,
                'story': story_data
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/poems/<path:poem_id>')
def get_poem(poem_id):
    try:
        # Remove 'root/' prefix if present
        poem_id = poem_id.replace('root/', '')
        file_path = os.path.join('data', f'{poem_id}.json')
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': f'Poem not found: {poem_id}'
            }), 404
            
        with open(file_path, 'r', encoding='utf-8') as f:
            poem_data = json.load(f)
            return jsonify({
                'success': True,
                'poem': poem_data
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/content')
def get_all_content():
    try:
        content = []
        data_dir = 'data'
        
        for filename in os.listdir(data_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    content.append({
                        'id': filename.replace('.json', ''),
                        'title': data.get('title', ''),
                        'type': data.get('type', 'story'),  # Default to story if type not specified
                        'content': data.get('content', ''),
                        'translation': data.get('translation', ''),
                        'vocabulary': data.get('vocabulary', [])
                    })
        
        return jsonify({
            'success': True,
            'stories': content
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 