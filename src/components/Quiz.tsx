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

  // Array of vibrant colors for flashcards
  const cardColors = [
    '#FF6B6B', // Coral Red
    '#4ECDC4', // Turquoise
    '#45B7D1', // Sky Blue
    '#96CEB4', // Mint Green
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

  useEffect(() => {
    console.log('Quiz component mounted with storyId:', storyId);
    fetchStoryAndGenerateQuestions();
  }, [storyId]);

  const fetchStoryAndGenerateQuestions = async () => {
    try {
      setLoading(true);
      console.log('Fetching story content for:', storyId);
      
      // Generate questions using story data
      console.log('Generating questions from story data...');
      const response = await fetch('http://localhost:5000/api/generate-questions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          storyId: storyId
        }),
      });

      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
      
      if (!data.success) {
        throw new Error('Failed to generate questions');
      }

      setFlashcards(data.questions);
      console.log('Flashcards set:', data.questions);
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
            color={cardColors[index % cardColors.length]}
          />
        ))}
      </div>
    </div>
  );
};

export default Quiz; 