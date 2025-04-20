import os
import json

def test_story_access():
    """Test if the story files can be accessed."""
    stories_dir = os.path.join('data', 'stories')
    
    print(f"Stories directory exists: {os.path.exists(stories_dir)}")
    if os.path.exists(stories_dir):
        print(f"Stories directory contents: {os.listdir(stories_dir)}")
        
        # Try to load a specific story
        story_file = os.path.join(stories_dir, 'baytakalluf-rishta.json')
        print(f"Story file exists: {os.path.exists(story_file)}")
        
        if os.path.exists(story_file):
            try:
                with open(story_file, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                print(f"Successfully loaded story: {story_data.get('title', 'Untitled')}")
            except Exception as e:
                print(f"Error loading story: {e}")
        
        # Try to load another story
        story_file = os.path.join(stories_dir, 'jheel-pay-aya-hathi.json')
        print(f"Story file exists: {os.path.exists(story_file)}")
        
        if os.path.exists(story_file):
            try:
                with open(story_file, 'r', encoding='utf-8') as f:
                    story_data = json.load(f)
                print(f"Successfully loaded story: {story_data.get('title', 'Untitled')}")
            except Exception as e:
                print(f"Error loading story: {e}")

if __name__ == '__main__':
    test_story_access() 