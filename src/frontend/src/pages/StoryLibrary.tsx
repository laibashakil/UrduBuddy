import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../styles/StoryLibrary.css';

interface Content {
  id: string;
  title: string;
  type: string;
}

const StoryLibrary: React.FC = () => {
  const [content, setContent] = useState<Content[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        console.log('Fetching content from API...');
        const response = await fetch('http://localhost:5000/api/stories');
        const data = await response.json();
        console.log('API response:', data);
        
        if (data.success) {
          setContent(data.stories);
          console.log('Loaded', data.stories.length, 'items');
        } else {
          setError(data.error || 'Failed to load content');
        }
      } catch (err) {
        console.error('Error fetching content:', err);
        setError('Failed to load content');
      } finally {
        setLoading(false);
      }
    };

    fetchContent();
  }, []);

  if (loading) return <div>Loading content...</div>;
  if (error) return <div>Error: {error}</div>;

  const stories = content.filter(item => item.type === 'story');
  const poems = content.filter(item => item.type === 'poem');

  return (
    <div className="story-library">
      <h1>Urdu Buddy Library</h1>
      
      <section className="content-section">
        <h2>Stories</h2>
        <div className="content-grid">
          {stories.map(story => (
            <Link 
              key={story.id} 
              to={`/story/${story.id}`}
              className="content-card"
            >
              <h3>{story.title}</h3>
            </Link>
          ))}
        </div>
      </section>

      <section className="content-section">
        <h2>Poems</h2>
        <div className="content-grid">
          {poems.map(poem => (
            <Link 
              key={poem.id} 
              to={`/story/${poem.id}`}
              className="content-card"
            >
              <h3>{poem.title}</h3>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
};

export default StoryLibrary; 