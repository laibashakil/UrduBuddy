from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

from llm_utils.llm_handler import llm_handler
from story_handler import StoryHandler

app = Flask(__name__)
# Enable CORS for all routes with more specific configuration
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"], "allow_headers": ["Content-Type"]}})

print("Initializing Flask server...")
story_handler = StoryHandler("data/stories")
print(f"Story handler: {story_handler}")
print(f"LLM handler: {llm_handler}")

def load_json_file(filename):
    """Load data from a JSON file"""
    file_path = os.path.join('data', filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

@app.route('/api/ask', methods=['POST'])
def ask_question():
    """Handle question asking endpoint"""
    data = request.get_json()
    
    if not data or 'question' not in data:
        return jsonify({'success': False, 'error': 'Question is required'}), 400
    
    question = data['question']
    story_id = data.get('story_id')
    
    try:
        if story_id:
            # Answer question about specific story
            result = story_handler.answer_question(story_id, question)
            return jsonify(result)  # Return the result directly as it already has the correct format
        else:
            return jsonify({
                'success': False,
                'error': 'Story ID is required'
            }), 400
    except Exception as e:
        print(f"Error processing question: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stories', methods=['GET'])
def get_stories():
    """Get all stories or filter by age group and/or type"""
    age_group = request.args.get('age_group')
    story_type = request.args.get('type')
    
    try:
        # Direct implementation to read all stories
        stories = []
        stories_dir = os.path.join('data', 'stories')
        
        print(f"Reading stories from directory: {stories_dir}")
        print(f"Directory exists: {os.path.exists(stories_dir)}")
        print(f"Directory contents: {os.listdir(stories_dir)}")
        
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
        app.logger.error(f"Error in get_stories: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stories/<path:story_id>', methods=['GET'])
def get_story(story_id):
    """Get a specific story by ID"""
    try:
        print(f"Received request for story ID: {story_id}")
        
        # Parse story ID to get file path
        parts = story_id.split('/')
        print(f"Split parts: {parts}")
        
        # Handle both formats: 'root/story-name' and just 'story-name'
        if len(parts) == 2:
            location, story_name = parts
        elif len(parts) == 1:
            # If it's just a story name without location, assume it's in the root directory
            story_name = parts[0]
        else:
            print(f"Invalid story ID format: {story_id}")
            return jsonify({
                'success': False,
                'error': 'Invalid story ID format'
            }), 400
            
        print(f"Story name: {story_name}")
        
        # Determine the actual file path
        stories_dir = os.path.join('data', 'stories')
        
        # List all files in the stories directory
        all_files = os.listdir(stories_dir)
        print(f"All files in stories directory: {all_files}")
        
        # Try to find the file with the exact name
        file_path = os.path.join(stories_dir, f"{story_name}.json")
        print(f"Looking for file at: {file_path}")
        
        # If file doesn't exist, try to find a matching file
        if not os.path.exists(file_path):
            print(f"File not found at exact path: {file_path}")
            
            # Try to find a file that starts with the same prefix
            matching_files = [f for f in all_files if f.startswith(story_name.split('-')[0]) and f.endswith('.json')]
            print(f"Matching files: {matching_files}")
            
            if matching_files:
                file_path = os.path.join(stories_dir, matching_files[0])
                print(f"Found matching file: {file_path}")
            else:
                # Try with 'j' instead of 'jh' and vice versa
                alt_name = story_name.replace('jheel', 'jheel').replace('jheel', 'jheel')
                alt_path = os.path.join(stories_dir, f"{alt_name}.json")
                print(f"Trying alternative path: {alt_path}")
                
                if os.path.exists(alt_path):
                    file_path = alt_path
                    print(f"Found file with alternative spelling: {alt_path}")
                else:
                    # Try with 'h' instead of 'j'
                    alt_name = story_name.replace('jheel', 'hheel')
                    alt_path = os.path.join(stories_dir, f"{alt_name}.json")
                    print(f"Trying another alternative path: {alt_path}")
                    
                    if os.path.exists(alt_path):
                        file_path = alt_path
                        print(f"Found file with another alternative spelling: {alt_path}")
                    else:
                        # Try with 'j' instead of 'h'
                        alt_name = story_name.replace('hheel', 'jheel')
                        alt_path = os.path.join(stories_dir, f"{alt_name}.json")
                        print(f"Trying yet another alternative path: {alt_path}")
                        
                        if os.path.exists(alt_path):
                            file_path = alt_path
                            print(f"Found file with yet another alternative spelling: {alt_path}")
                        else:
                            # If all else fails, try to find any file that contains the story name
                            for file in all_files:
                                if story_name in file and file.endswith('.json'):
                                    file_path = os.path.join(stories_dir, file)
                                    print(f"Found file containing story name: {file_path}")
                                    break
        
        print(f"Final file path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Story not found at: {file_path}")
            return jsonify({
                'success': False,
                'error': f'Story not found: {story_id}'
            }), 404
            
        # Read the story file
        with open(file_path, 'r', encoding='utf-8') as f:
            story_data = json.load(f)
            
        print(f"Successfully loaded story: {story_name}")
        return jsonify({
            'success': True,
            'story': story_data
        })
    except Exception as e:
        print(f"Error in get_story: {str(e)}")
        app.logger.error(f"Error in get_story: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/vocabulary', methods=['GET'])
def get_vocabulary():
    """Get vocabulary data"""
    try:
        data = load_json_file('vocab.json')
        if data and 'words' in data:
            return jsonify({
                'success': True,
                'vocabulary': data['words']
            })
        return jsonify({
            'success': False,
            'error': 'Vocabulary data not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/alphabet', methods=['GET'])
def get_alphabet():
    """Get alphabet data"""
    try:
        data = load_json_file('alphabet.json')
        if data and 'letters' in data:
            return jsonify({
                'success': True,
                'alphabet': data['letters']
            })
        return jsonify({
            'success': False,
            'error': 'Alphabet data not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/colors-shapes', methods=['GET'])
def get_colors_shapes():
    """Get colors and shapes data"""
    try:
        data = load_json_file('colors_shapes.json')
        if data:
            return jsonify({
                'success': True,
                'colors': data.get('colors', []),
                'shapes': data.get('shapes', [])
            })
        return jsonify({
            'success': False,
            'error': 'Colors and shapes data not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stories/<story_id>/ask', methods=['POST'])
def ask_story_question(story_id):
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'Question is required'}), 400
            
        # Get the answer using the story handler
        result = story_handler.answer_question(story_id, question)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stories/<path:story_id>/chat', methods=['POST'])
def chat_about_story(story_id):
    try:
        # Get message from request
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({
                "success": False,
                "error": "Message is required"
            }), 400
            
        message = data['message']
        
        # Get story content
        story_data = story_handler.get_story_content(story_id)
        if not story_data:
            return jsonify({
                "success": False,
                "error": "Story not found"
            }), 404
            
        # Extract the actual content from story data
        story_content = story_data.get('content', '')
        if not story_content:
            return jsonify({
                "success": False,
                "error": "Story has no content"
            }), 400
            
        # Get response from LLM
        response = llm_handler.chat_about_story(story_content, message)
        
        if not response.get('success'):
            return jsonify({
                "success": False,
                "error": "Failed to generate response"
            }), 500
            
        return jsonify({
            "success": True,
            "response": response.get('response', '')
        })
        
    except Exception as e:
        print(f"Error in chat_about_story: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 