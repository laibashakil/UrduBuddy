import React, { useState, useEffect } from 'react';
import '../styles/StoryReader.css';
import StoryQuestion from './StoryQuestion';

interface StoryData {
  title: string;
  content: string;
  age_group?: string;
  ageGroup?: string;
  language: string;
  type?: string;
}

interface StoryReaderProps {
  storyId: string;
}

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const StoryReader: React.FC<StoryReaderProps> = ({ storyId }) => {
  const [story, setStory] = useState<StoryData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch story on component mount
  useEffect(() => {
    const fetchStory = async () => {
      try {
        setLoading(true);
        console.log(`Fetching story with ID: ${storyId}`);
        
        // Check if storyId is valid
        if (!storyId) {
          console.error('Invalid story ID:', storyId);
          setError('Invalid story ID');
          setLoading(false);
          return;
        }
        
        // Add root/ prefix if not present
        const fullStoryId = storyId.startsWith('root/') ? storyId : `root/${storyId}`;
        console.log(`Using full story ID for fetch: ${fullStoryId}`);
        
        // Use the full URL for the Flask server
        const response = await fetch(`${API_BASE_URL}/api/stories/${fullStoryId}`);
        console.log('Response status:', response.status);
        
        const data = await response.json();
        console.log('Story API response:', data);
        
        if (data.success) {
          console.log('Setting story data:', data.story);
          setStory(data.story);
        } else {
          console.error('API error:', data.error);
          setError(data.error || 'Failed to load story');
        }
      } catch (err) {
        console.error('Error fetching story:', err);
        setError('Error loading story. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    if (storyId) {
      fetchStory();
    } else {
      setError('No story ID provided');
    }
  }, [storyId]);

  if (loading && !story) {
    return <div className="loading">Loading story... {storyId}</div>;
  }

  if (error && !story) {
    return <div className="error">Error: {error} (Story ID: {storyId})</div>;
  }

  if (!story) {
    return <div className="error">Story not found (ID: {storyId})</div>;
  }

  // Check for valid story content
  if (!story.content) {
    return <div className="error">This story has no content (ID: {storyId})</div>;
  }

  // Determine if this is a poem or a story
  const isPoem = story.type?.toLowerCase() === 'poem';

  // Format the story content with line breaks
  const formattedContent = story.content.split('\n').map((line, index) => (
    <React.Fragment key={index}>
      {line}
      <br />
    </React.Fragment>
  ));

  // Add root/ prefix for the chat component
  const fullStoryId = storyId.startsWith('root/') ? storyId : `root/${storyId}`;

  return (
    <div className="story-reader">
      <div className="story-header">
        <h1 className="story-title">{story.title}</h1>
      </div>
      <div className={`story-content ${isPoem ? 'poem-content' : ''}`} dir="rtl">
        {formattedContent}
      </div>

      {/* Add the chat component */}
      <StoryQuestion 
        storyId={fullStoryId}
        storyContent={story.content}
      />
    </div>
  );
};

export default StoryReader; 