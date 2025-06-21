import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/QuizLibrary.css';

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
  const getRandomColor = (id: string) => {
    const kidFriendlyColors = [
      '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD',
      '#D4A5A5', '#9B59B6', '#E67E22', '#1ABC9C', '#F1C40F',
      '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#8E44AD'
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
    <div className="quiz-library">
      <div className="quiz-library-header">
        <h1 className="urdu urdu-xlarge">اردو کویز</h1>
        <p className="subtitle urdu urdu-medium">ہمارے کہانیوں کے کویز</p>
      </div>

      {error && <div className="error">{error}</div>}

      {stories.length === 0 ? (
        <div className="no-content">
          <p>No stories available for quizzes.</p>
        </div>
      ) : (
        <div className="quiz-grid">
          {stories.map(story => {
            return (
              <div key={story.id} className="quiz-card">
                <div className="quiz-card-header" style={{ backgroundColor: getRandomColor(story.id) }}></div>
                <div className="quiz-card-content">
                  <h2 className="quiz-card-title urdu urdu-medium">{story.title}</h2>
                  <Link to={getQuizRoute(story.id)} className="quiz-card-button">
                    Start Quiz
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default QuizLibrary; 