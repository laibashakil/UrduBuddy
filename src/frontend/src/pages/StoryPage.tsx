import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ChatInterface from '../components/ChatInterface';
import '../styles/ChatInterface.css';

interface Story {
  title: string;
  content: string;
  type: string;
}

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const StoryPage: React.FC = () => {
  const { storyId } = useParams<{ storyId: string }>();
  const [story, setStory] = useState<Story | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStory = async () => {
      try {
        // Add root/ prefix if not present
        const fullStoryId = storyId?.startsWith('root/') ? storyId : `root/${storyId}`;
        console.log(`Fetching story with ID: ${fullStoryId}`);
        
        // Use the full URL for the Flask server
        const response = await fetch(`${API_BASE_URL}/api/stories/${fullStoryId}`);
        const data = await response.json();
        
        if (data.success) {
          setStory(data.story);
        } else {
          setError(data.error || 'Failed to load story');
        }
      } catch (err) {
        console.error('Error fetching story:', err);
        setError('Failed to load story');
      } finally {
        setLoading(false);
      }
    };

    if (storyId) {
      fetchStory();
    }
  }, [storyId]);

  if (loading) return <div>Loading story...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!story) return <div>Story not found</div>;

  return (
    <div className="story-page">
      <h1>{story.title}</h1>
      <div className="story-content">
        {story.content.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      <ChatInterface storyId={storyId || ''} />
    </div>
  );
};

export default StoryPage; 