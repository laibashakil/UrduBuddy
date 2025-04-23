import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import StoryChat from '../components/StoryChat';
import '../styles/StoryDetail.css';

interface Content {
  id: string;
  title: string;
  content: string;
  type: 'story' | 'poem';
}

const StoryDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [content, setContent] = useState<Content | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchContent = async () => {
      try {
        const response = await fetch(`http://localhost:5000/api/stories/${id}`);
        if (!response.ok) {
          throw new Error('Content not found');
        }
        const data = await response.json();
        if (data.success && data.story) {
          setContent({
            id: id || '',
            title: data.story.title || 'Untitled',
            content: data.story.content || '',
            type: data.story.type || 'story'
          });
        } else {
          throw new Error('Invalid story data');
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchContent();
    }
  }, [id]);

  if (loading) {
    return <div className="story-detail loading">Loading...</div>;
  }

  if (error || !content) {
    return (
      <div className="story-detail error">
        <p>{error || 'Content not found'}</p>
        <button onClick={() => navigate('/library')}>Back to Library</button>
      </div>
    );
  }

  return (
    <div className="story-detail">
      <button className="back-button" onClick={() => navigate('/library')}>
        Back to Library
      </button>
      <h1>{content.title}</h1>
      <div className="content-type">{content.type}</div>
      <div className="content-body">
        {content.content.split('\n').map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      <div className="chat-section">
        <h2>کہانی کے بارے میں پوچھیں</h2>
        <StoryChat storyId={content.id} />
      </div>
    </div>
  );
};

export default StoryDetail; 