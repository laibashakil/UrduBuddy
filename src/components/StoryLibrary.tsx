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
  const [filteredContent, setFilteredContent] = useState<Content[]>([]);
  const [selectedType, setSelectedType] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // Content type options
  const contentTypes = [
    { id: '', label: 'All Content' },
    { id: 'story', label: 'Stories' },
    { id: 'poem', label: 'Poems' }
  ];

  // Fetch content on component mount
  useEffect(() => {
    fetchContent();
  }, []);

  // Apply filters when selection changes
  useEffect(() => {
    let filtered = [...content];
    
    // Filter by content type if selected
    if (selectedType) {
      filtered = filtered.filter(item => item.type?.toLowerCase() === selectedType);
    }
    
    setFilteredContent(filtered);
  }, [selectedType, content]);

  const fetchContent = async () => {
    try {
      setLoading(true);
      console.log('Fetching content from API...');
      // Use the full URL for the Flask server
      const response = await fetch(`${API_BASE_URL}/api/stories`);
      const data = await response.json();
      
      console.log('API response:', data);
      
      if (data.success) {
        console.log(`Loaded ${data.stories?.length || 0} items`);
        setContent(data.stories || []);
        setFilteredContent(data.stories || []);
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
    // Use different color palettes for stories and poems
    const storyColors = [
      '#4682B4', // SteelBlue
      '#2E8B57', // SeaGreen
      '#8B4513', // SaddleBrown
      '#A52A2A', // Brown
      '#800000', // Maroon
    ];
    
    const poemColors = [
      '#800080', // Purple
      '#4B0082', // Indigo
      '#483D8B', // DarkSlateBlue
      '#9370DB', // MediumPurple
      '#8A2BE2', // BlueViolet
    ];
    
    const colors = type === 'poem' ? poemColors : storyColors;
    const sum = id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[sum % colors.length];
  };

  // Get the correct route for the content item
  const getContentRoute = (item: Content) => {
    // Use /story/ route for both stories and poems
    return `/story/${item.id}`;
  };

  if (loading && content.length === 0) {
    return <div className="loading">Loading content...</div>;
  }

  return (
    <div className="content-library">
      <div className="library-header">
        <h1>Urdu Content Library</h1>
        <p className="subtitle">Explore our collection of stories and poems</p>
      </div>

      <div className="filter-section">
        <div className="filters">
          <div className="filter">
            <label>Content type:</label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="content-type-select"
            >
              {contentTypes.map(type => (
                <option key={type.id} value={type.id}>{type.label}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {filteredContent.length === 0 ? (
        <div className="no-content">
          <p>No content matches your selected filters.</p>
        </div>
      ) : (
        <div className="content-grid">
          {filteredContent.map(item => {
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
                  <div className="content-type">
                    {item.type === 'poem' ? 'نظم' : 'کہانی'}
                  </div>
                  <div className="content-age">
                    Age: {item.age_group}
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

export default ContentLibrary; 