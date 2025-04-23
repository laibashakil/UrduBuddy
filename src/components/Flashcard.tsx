import React, { useState } from 'react';
import '../styles/Flashcard.css';

interface FlashcardProps {
  question: string;
  answer: string;
}

const Flashcard: React.FC<FlashcardProps> = ({ question, answer }) => {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div 
      className={`flashcard ${isFlipped ? 'flipped' : ''}`}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div className="flashcard-inner">
        <div className="flashcard-front">
          <h3>{question}</h3>
          <p className="hint">Click to see answer</p>
        </div>
        <div className="flashcard-back">
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      </div>
    </div>
  );
};

export default Flashcard; 