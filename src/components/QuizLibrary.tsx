import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/StoryLibrary.css';

interface Story {
  id: string;
  title: string;
  age_group: string;
  language: string;
  type: string;
}

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const QuizLibrary: React.FC = () => {
  const [stories, setStories] = useState<Story[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Fetch stories on component mount
  useEffect(() => {
    fetchStories();
  }, []);

  const fetchStories = async () => {
    try {
      setLoading(true);
      console.log('Fetching stories from API...');
      const response = await fetch(`${API_BASE_URL}/api/stories`);
      const data = await response.json();
      
      console.log('API response:', data);
      
      if (data.success) {
        console.log(`Loaded ${data.stories?.length || 0} items`);
        setStories(data.stories || []);
      } else {
        console.error('API returned error:', data.error);
        setError(data.error || 'Failed to load stories');
      }
    } catch (err) {
      console.error('Error fetching stories:', err);
      setError('Error loading stories. Please make sure the server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Generate a random color for visual variety
  const getRandomColor = (id: string, type: string) => {
    const kidFriendlyColors = [
      '#FF6B6B', // Coral Red
      '#4ECDC4', // Turquoise
      '#45B7D1', // Sky Blue
      '#96CEB4', // Mint Green
      '#FFEEAD', // Soft Yellow
      '#D4A5A5', // Dusty Rose
      '#9B59B6', // Purple
      '#E67E22', // Orange
      '#1ABC9C', // Teal
      '#F1C40F', // Yellow
      '#E74C3C', // Red
      '#3498DB', // Blue
      '#2ECC71', // Green
      '#F39C12', // Orange
      '#8E44AD'  // Purple
    ];
    
    const sum = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return kidFriendlyColors[sum % kidFriendlyColors.length];
  };

  // Get the correct route for the quiz item
  const getQuizRoute = (storyId: string) => {
    return `/quiz/${storyId}`;
  };

  if (loading && stories.length === 0) {
    return <div className="loading">Loading stories...</div>;
  }

  return (
    <div className="content-library">
      <div className="library-header">
        <h1 className="urdu urdu-xlarge">اردو کویز</h1>
        <p className="subtitle urdu urdu-medium">ہمارے کہانیوں کے کویز</p>
      </div>

      {error && <div className="error">{error}</div>}

      {stories.length === 0 ? (
        <div className="no-content">
          <p>No stories available for quizzes.</p>
        </div>
      ) : (
        <div className="content-grid">
          {stories.map(story => {
            return (
              <Link 
                to={getQuizRoute(story.id)}
                key={story.id} 
                className={`content-item ${story.type.toLowerCase()}`}
                style={{ backgroundColor: getRandomColor(story.id, story.type) }}
              >
                <div className="content-spine"></div>
                <div className="content-cover">
                  <h2 className="content-title">{story.title}</h2>
                  <p className="quiz-label">کویز</p>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default QuizLibrary; 