import React, { useState } from 'react';
import '../styles/Flashcard.css';

interface FlashcardProps {
  question: string;
  answer: string;
  color: string;
}

const Flashcard: React.FC<FlashcardProps> = ({ question, answer, color }) => {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div 
      className={`flashcard ${isFlipped ? 'flipped' : ''}`}
      onClick={() => setIsFlipped(!isFlipped)}
      style={{ '--card-color': color } as React.CSSProperties}
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