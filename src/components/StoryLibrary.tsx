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

const StoryLibrary: React.FC = () => {
  const [stories, setStories] = useState<Story[]>([]);
  const [filteredStories, setFilteredStories] = useState<Story[]>([]);
  const [selectedType, setSelectedType] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Content type options
  const contentTypes = [
    { id: '', label: 'All Types' },
    { id: 'story', label: 'Stories' },
    { id: 'poem', label: 'Poems' }
  ];

  // Fetch stories on component mount
  useEffect(() => {
    fetchStories();
  }, []);

  // Apply filters when selection changes
  useEffect(() => {
    let filtered = [...stories];
    
    // Filter by content type if selected
    if (selectedType) {
      filtered = filtered.filter(story => story.type?.toLowerCase() === selectedType);
    }
    
    setFilteredStories(filtered);
  }, [selectedType, stories]);

  const fetchStories = async () => {
    try {
      setLoading(true);
      console.log('Fetching stories from API...');
      // Use the full URL for the Flask server
      const response = await fetch(`${API_BASE_URL}/api/stories`);
      const data = await response.json();
      
      console.log('API response:', data);
      
      if (data.success) {
        console.log(`Loaded ${data.stories?.length || 0} stories`);
        setStories(data.stories || []);
        setFilteredStories(data.stories || []);
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

  // Generate a random book color for visual variety
  const getRandomBookColor = (id: string) => {
    // Use the story ID to generate a consistent color for each story
    const colors = [
      '#8B4513', // SaddleBrown
      '#A52A2A', // Brown
      '#800000', // Maroon
      '#2E8B57', // SeaGreen
      '#4682B4', // SteelBlue
      '#483D8B', // DarkSlateBlue
      '#800080', // Purple
      '#4B0082', // Indigo
      '#556B2F', // DarkOliveGreen
      '#B8860B', // DarkGoldenrod
    ];
    
    const sum = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[sum % colors.length];
  };

  if (loading && stories.length === 0) {
    return <div className="loading">Loading stories...</div>;
  }

  return (
    <div className="story-library">
      <div className="library-header">
        <h1>Urdu Stories Library</h1>
      </div>

      <div className="filter-section">
        <div className="filters">
          <div className="filter">
            <label>Content type:</label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
            >
              {contentTypes.map(type => (
                <option key={type.id} value={type.id}>{type.label}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {filteredStories.length === 0 ? (
        <div className="no-stories">
          <p>No stories match your selected filters.</p>
        </div>
      ) : (
        <div className="bookshelf">
          {filteredStories.map(story => {
            // Extract the story name without the 'root/' prefix for the URL
            const urlId = story.id.replace('root/', '');
            console.log(`Story ${story.title} - ID: ${urlId}`);
            
            return (
              <Link 
                to={`/story/${urlId}`} 
                key={story.id} 
                className="book"
                style={{ backgroundColor: getRandomBookColor(story.id) }}
              >
                <div className="book-spine"></div>
                <div className="book-cover">
                  <h2 className="book-title">{story.title}</h2>
                  <div className="book-type">
                    {story.type === 'poem' ? 'نظم' : 'کہانی'}
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default StoryLibrary; 