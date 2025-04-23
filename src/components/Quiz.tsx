import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/Quiz.css';
import Flashcard from './Flashcard';

interface FlashcardData {
  question: string;
  answer: string;
}

interface QuizProps {
  storyId: string;
}

const Quiz: React.FC<QuizProps> = ({ storyId }) => {
  const [flashcards, setFlashcards] = useState<FlashcardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    console.log('Quiz component mounted with storyId:', storyId);
    fetchStoryAndGenerateQuestions();
  }, [storyId]);

  const fetchStoryAndGenerateQuestions = async () => {
    try {
      setLoading(true);
      console.log('Fetching story content for:', storyId);
      
      // First, fetch the story content
      const storyResponse = await fetch(`http://localhost:5000/api/stories/${storyId}`);
      console.log('Story response status:', storyResponse.status);
      const storyData = await storyResponse.json();
      console.log('Story data:', storyData);
      
      if (!storyData.success) {
        throw new Error('Failed to fetch story');
      }

      const storyContent = storyData.story.content;
      console.log('Story content length:', storyContent.length);
      
      // Now generate questions using Cohere
      console.log('Generating questions with Cohere...');
      const cohereResponse = await fetch('http://localhost:5000/api/generate-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          story: storyContent,
          numQuestions: 5
        }),
      });

      console.log('Cohere response status:', cohereResponse.status);
      const cohereData = await cohereResponse.json();
      console.log('Cohere data:', cohereData);
      
      if (!cohereData.success) {
        throw new Error('Failed to generate questions');
      }

      setFlashcards(cohereData.questions);
      console.log('Flashcards set:', cohereData.questions);
    } catch (err) {
      console.error('Error:', err);
      setError('Failed to load quiz. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Generating flashcards...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (flashcards.length === 0) {
    return <div className="error">No flashcards available for this story.</div>;
  }

  return (
    <div className="quiz-container">
      <div className="quiz-header">
        <h2>کہانی کے سوالات</h2>
        <p>کلپ کارڈز پر کلک کریں جواب دیکھنے کے لیے</p>
      </div>

      <div className="flashcards-container">
        {flashcards.map((card, index) => (
          <Flashcard
            key={index}
            question={card.question}
            answer={card.answer}
          />
        ))}
      </div>
    </div>
  );
};

export default Quiz; 