import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/StoryLibrary.css';

interface Content {
  id: string;
  title: string;
  age_group: string;
  language: string;
  type: string;
}

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const ContentLibrary: React.FC = () => {
  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Fetch content on component mount
  useEffect(() => {
    fetchContent();
  }, []);

  const fetchContent = async () => {
    try {
      setLoading(true);
      console.log('Fetching content from API...');
      const response = await fetch(`${API_BASE_URL}/api/stories`);
      const data = await response.json();
      
      console.log('API response:', data);
      
      if (data.success) {
        console.log(`Loaded ${data.stories?.length || 0} items`);
        setContent(data.stories || []);
      } else {
        console.error('API returned error:', data.error);
        setError(data.error || 'Failed to load content');
      }
    } catch (err) {
      console.error('Error fetching content:', err);
      setError('Error loading content. Please make sure the server is running.');
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

  // Get the correct route for the content item
  const getContentRoute = (item: Content) => {
    return `/story/${item.id}`;
  };

  if (loading && content.length === 0) {
    return <div className="loading">Loading content...</div>;
  }

  return (
    <div className="content-library">
      <div className="library-header">
        <h1 className="urdu urdu-xlarge">اردو کتب خانہ</h1>
        <p className="subtitle urdu urdu-medium">ہماری کہانیوں کا مجموعہ</p>
      </div>

      {error && <div className="error">{error}</div>}

      {content.length === 0 ? (
        <div className="no-content">
          <p>No content available.</p>
        </div>
      ) : (
        <div className="content-grid">
          {content.map(item => {
            return (
              <Link 
                to={getContentRoute(item)}
                key={item.id} 
                className={`content-item ${item.type.toLowerCase()}`}
                style={{ backgroundColor: getRandomColor(item.id, item.type) }}
              >
                <div className="content-spine"></div>
                <div className="content-cover">
                  <h2 className="content-title">{item.title}</h2>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ContentLibrary; 