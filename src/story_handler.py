import os
import json
from typing import Dict, List, Any, Optional
import re
from llm_utils.llm_handler import chat_about_story

class StoryHandler:
    def __init__(self, data_dir: str = "data/stories"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Cache for story data to avoid frequent disk reads
        self.story_cache = {}
        
    def get_all_stories(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all available stories
        
        Returns:
            List of story metadata objects
        """
        stories = []
        
        # First look for stories directly in the data directory
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json') and os.path.isfile(os.path.join(self.data_dir, filename)):
                file_path = os.path.join(self.data_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        story_data = json.load(f)
                        
                    # Add metadata for the story list
                    stories.append({
                        "id": f"root/{filename[:-5]}",  # Remove .json extension
                        "title": story_data.get("title", "Untitled"),
                        "age_group": story_data.get("ageGroup", story_data.get("age_group", "")),
                        "language": story_data.get("language", "urdu"),
                        "type": story_data.get("type", "story").lower()  # Default to story if not specified
                    })
                except Exception as e:
                    print(f"Error loading story {file_path}: {e}")
        
        # Walk through all subdirectories
        for subdir in os.listdir(self.data_dir):
            subdir_path = os.path.join(self.data_dir, subdir)
            if not os.path.isdir(subdir_path):
                continue
                
            # Look for story files in this subdirectory
            for filename in os.listdir(subdir_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(subdir_path, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            story_data = json.load(f)
                            
                        # Add metadata for the story list
                        stories.append({
                            "id": f"{subdir}/{filename[:-5]}",  # Remove .json extension
                            "title": story_data.get("title", "Untitled"),
                            "age_group": story_data.get("ageGroup", story_data.get("age_group", "")),
                            "language": story_data.get("language", "urdu"),
                            "type": story_data.get("type", "story").lower()  # Default to story if not specified
                        })
                    except Exception as e:
                        print(f"Error loading story {file_path}: {e}")
        
        return stories
    
    def get_stories_by_age(self, age_group: str) -> List[Dict[str, Any]]:
        """
        Get stories filtered by age group
        
        Args:
            age_group: Age group to filter by
            
        Returns:
            List of story metadata objects
        """
        return [s for s in self.get_all_stories() if s["age_group"] == age_group]
    
    def get_story_content(self, story_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the full content of a story by its ID
        
        Args:
            story_id: Story ID in format 'root/story_name' or just 'story_name'
            
        Returns:
            Story data or None if not found
        """
        # Check if in cache first
        if story_id in self.story_cache:
            return self.story_cache[story_id]
            
        # Parse story ID to get file path
        parts = story_id.split('/')
        if len(parts) == 2:
            # Format: root/story_name or subdirectory/story_name
            location, story_name = parts
        else:
            # Format: story_name
            story_name = story_id
            
        # Convert underscores to hyphens in the story name
        story_name = story_name.replace('_', '-')
        
        # Try loading from root directory first
        file_path = os.path.join(self.data_dir, f"{story_name}.json")
        
        if not os.path.exists(file_path) and len(parts) == 2:
            # If not found in root and we have a location, try the subdirectory
            file_path = os.path.join(self.data_dir, parts[0], f"{story_name}.json")
        
        # If still not found, try with different spellings or formats
        if not os.path.exists(file_path):
            # Try with different spellings (e.g., jheel vs hheel)
            alt_name = story_name.replace('jheel', 'hheel').replace('hheel', 'jheel')
            alt_path = os.path.join(self.data_dir, f"{alt_name}.json")
            
            if os.path.exists(alt_path):
                file_path = alt_path
            else:
                # Try with different formats (e.g., with or without hyphens)
                alt_name = story_name.replace('-', '_')
                alt_path = os.path.join(self.data_dir, f"{alt_name}.json")
                
                if os.path.exists(alt_path):
                    file_path = alt_path
        
        if not os.path.exists(file_path):
            print(f"Story not found: {file_path}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
                
            # Cache the story data
            self.story_cache[story_id] = story_data
            return story_data
        except Exception as e:
            print(f"Error loading story {file_path}: {e}")
            return None
    
    def answer_question(self, story_id: str, question: str) -> dict:
        """Answer a question about a specific story using direct prompt."""
        try:
            # Validate inputs
            if not story_id or not question:
                return {
                    'error': 'Story ID and question are required',
                    'success': False,
                    'found': False
                }
            
            # Sanitize inputs
            question = question.strip()
            if len(question) > 500:  # Limit question length
                return {
                    'error': 'Question is too long. Please keep it under 500 characters.',
                    'success': False,
                    'found': False
                }
            
            # Get the story content
            story_data = self.get_story_content(story_id)
            if not story_data:
                return {
                    'error': 'Story not found',
                    'success': False,
                    'found': False
                }
            
            # Get the story content
            story_content = story_data.get('content', '')
            if not story_content:
                return {
                    'error': 'Story has no content',
                    'success': False,
                    'found': True
                }
            
            # For title questions, just use the title
            if 'عنوان' in question or 'title' in question.lower():
                story_content = story_data.get('title', '')
            
            # For summary questions, use the summary if available
            elif 'خلاصہ' in question or 'summary' in question.lower():
                story_content = story_data.get('summary', story_content)
            
            # For other questions, use the full content but limit length
            if len(story_content) > 10000:  # Limit story length
                story_content = story_content[:10000]
            
            # Use the LLM handler to answer the question with the story content
            llm_response = chat_about_story(story_content, question)
            
            if not llm_response.get('success'):
                return {
                    'error': 'Failed to generate response',
                    'success': False,
                    'found': True
                }
            
            return {
                'success': True,
                'found': True,
                'response': llm_response.get('response', ''),
                'story_title': story_data.get('title', 'Untitled')
            }
            
        except Exception as e:
            print(f"Error in answer_question: {e}")
            return {
                'error': str(e),
                'success': False,
                'found': False,
                'response': 'معذرت، میں اس وقت سوالات کا جواب نہیں دے سکتا۔'
            }

# Initialize the story handler
story_handler = StoryHandler() 