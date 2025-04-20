from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import sys

# Set console encoding to UTF-8 to handle Urdu characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__, template_folder='templates')
CORS(app)  # Enable CORS for all routes

def load_json_file(filename):
    """Load data from a JSON file"""
    file_path = os.path.join('data', filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/stories', methods=['GET'])
def get_stories():
    """Get all stories or filter by age group and/or type"""
    age_group = request.args.get('age_group')
    story_type = request.args.get('type')
    
    try:
        # Direct implementation to read all stories
        stories = []
        stories_dir = os.path.join('data', 'stories')
        
        # Read stories from the root directory
        for filename in os.listdir(stories_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(stories_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            story_data = json.load(f)
                        
                        # Extract story metadata
                        story_title = story_data.get('title', 'Untitled')
                        story_age_group = story_data.get('ageGroup', story_data.get('age_group', ''))
                        story_language = story_data.get('language', 'urdu')
                        story_type_value = story_data.get('type', 'story').lower()
                        
                        # Create story metadata object
                        stories.append({
                            'id': f'root/{os.path.splitext(filename)[0]}',
                            'title': story_title,
                            'age_group': story_age_group,
                            'language': story_language,
                            'type': story_type_value
                        })
                    except Exception as e:
                        print(f"Error reading story file {file_path}: {e}")
        
        # Apply age group filter if specified
        if age_group:
            stories = [s for s in stories if s.get('age_group') == age_group]
            
        # Apply type filter if specified
        if story_type:
            stories = [s for s in stories if s.get('type', '').lower() == story_type.lower()]
            
        return jsonify({
            'success': True,
            'stories': stories
        })
    except Exception as e:
        error_msg = f"Error in get_stories: {str(e)}"
        print(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/stories/<string:story_id>', methods=['GET'])
def get_story(story_id):
    """Get a specific story by ID"""
    try:
        # Avoid printing Urdu characters directly to prevent encoding issues
        print(f"Received request for story with ID: {story_id}")
        
        # Parse story ID to get file path
        parts = story_id.split('/')
        print(f"Parts after splitting: {parts}")
        
        # Special case - if it's just a simple ID without a slash, assume it's in root directory
        if len(parts) == 1:
            location = "root"
            story_name = parts[0]
            print(f"Single part ID detected, treating as root/{story_name}")
        elif len(parts) == 2:
            location, story_name = parts
        else:
            return jsonify({
                'success': False,
                'error': f'Invalid story ID format: {story_id}, parts: {parts}'
            }), 400
        
        print(f"Looking for story in location: {location}, name: {story_name}")
            
        # Determine the actual file path
        stories_dir = os.path.join('data', 'stories')
        if location == 'root':
            # Story in root directory
            file_path = os.path.join(stories_dir, f"{story_name}.json")
        else:
            # Story in a subdirectory
            file_path = os.path.join(stories_dir, location, f"{story_name}.json")
        
        print(f"Checking for file at: {file_path}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            # Try another approach - look for the file directly in the root directory
            direct_path = os.path.join(stories_dir, f"{story_id}.json")
            print(f"Trying direct path: {direct_path}")
            
            if os.path.exists(direct_path):
                file_path = direct_path
                print(f"Found file at direct path: {file_path}")
            else:
                return jsonify({
                    'success': False,
                    'error': f'Story not found: {story_id}, tried paths: {file_path}, {direct_path}'
                }), 404
            
        # Read the story file
        with open(file_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            
        print(f"Successfully loaded story with ID: {story_id}")
        return jsonify({
            'success': True,
            'story': story_data
        })
    except Exception as e:
        error_msg = f"Error in get_story: {str(e)}"
        print(error_msg)
        app.logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Simplified question answering that returns dummy response"""
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'success': False, 'error': 'Question is required'}), 400
    
    # Just return a dummy answer
    return jsonify({
        'success': True,
        'response': 'مجھے معاف کیجیے، میں اس وقت سوالات کا جواب نہیں دے سکتا۔',
        'story_title': '',
        'found': True
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 