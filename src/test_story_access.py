import os
import json

def test_story_access():
    """Test if story files can be accessed correctly"""
    stories_dir = os.path.join('data', 'stories')
    print(f"Testing access to stories directory: {stories_dir}")
    print(f"Directory exists: {os.path.exists(stories_dir)}")
    
    if not os.path.exists(stories_dir):
        print(f"ERROR: Stories directory does not exist: {stories_dir}")
        return
    
    print(f"Directory contents: {os.listdir(stories_dir)}")
    
    # Test accessing a specific story
    story_name = "ek-acha-dost"
    file_path = os.path.join(stories_dir, f"{story_name}.json")
    print(f"Testing access to story file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
            print(f"Successfully loaded story: {story_name}")
            print(f"Story title: {story_data.get('title', 'No title')}")
            print(f"Story content length: {len(story_data.get('content', ''))}")
        except Exception as e:
            print(f"Error loading story: {e}")
    else:
        print(f"ERROR: Story file does not exist: {file_path}")
    
    # Test accessing another story
    story_name = "jheel-pay-aya-hathi"
    file_path = os.path.join(stories_dir, f"{story_name}.json")
    print(f"Testing access to story file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                story_data = json.load(f)
            print(f"Successfully loaded story: {story_name}")
            print(f"Story title: {story_data.get('title', 'No title')}")
            print(f"Story content length: {len(story_data.get('content', ''))}")
        except Exception as e:
            print(f"Error loading story: {e}")
    else:
        print(f"ERROR: Story file does not exist: {file_path}")

if __name__ == "__main__":
    test_story_access() 