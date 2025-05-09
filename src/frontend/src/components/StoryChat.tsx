import React, { useState, useRef, useEffect } from 'react';
import '../styles/StoryChat.css';

interface Message {
  text: string;
  isUser: boolean;
}

interface StoryChatProps {
  storyId: string;
}

const commonQuestions = [
  "کہانی کا عنوان کیا ہے؟",
  "کہانی کا خلاصہ بتائیں",
  "کہانی کا سبق کیا ہے؟",
  "کہانی کے اہم کردار کون ہیں؟",
  "کہانی کا اختتام کیسے ہوا؟"
];

const StoryChat: React.FC<StoryChatProps> = ({ storyId }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [abortController, setAbortController] = useState<AbortController | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [input]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setIsLoading(true);

    // Create new AbortController for this request
    const controller = new AbortController();
    setAbortController(controller);

    try {
      const response = await fetch(`http://localhost:5000/api/stories/${storyId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
        signal: controller.signal
      });

      const data = await response.json();
      if (data.success) {
        setMessages(prev => [...prev, { text: data.response, isUser: false }]);
      } else {
        setMessages(prev => [...prev, { 
          text: 'معذرت، میں آپ کے سوال کا جواب نہیں دے سکا۔', 
          isUser: false 
        }]);
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        setMessages(prev => [...prev, { 
          text: 'جواب روک دیا گیا۔', 
          isUser: false 
        }]);
      } else {
        setMessages(prev => [...prev, { 
          text: 'معذرت، ایک خرابی پیش آگئی ہے۔', 
          isUser: false 
        }]);
      }
    } finally {
      setIsLoading(false);
      setAbortController(null);
    }
  };

  const handleStop = () => {
    if (abortController) {
      abortController.abort();
      setIsLoading(false);
      setAbortController(null);
    }
  };

  const handleQuestionClick = (question: string) => {
    setInput(question);
  };

  return (
    <div className="story-chat">
      <div className="chat-header">
        <h2>کہانی کے بارے میں  کریں</h2>
        <p className="language-hint">آپ انگریزی یااردو میں سوال پوچھ سکتے ہیں۔</p>
      </div>

      <div className="common-questions">
        {commonQuestions.map((question, index) => (
          <button
            key={index}
            className="question-button"
            onClick={() => handleQuestionClick(question)}
            disabled={isLoading}
          >
            {question}
          </button>
        ))}
      </div>
      
      <div className="chat-container" ref={chatContainerRef}>
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${message.isUser ? 'user' : 'bot'}`}
          >
            {message.text}
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <div className="loading-dots">...</div>
          </div>
        )}
      </div>

      <div className="input-container">
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          placeholder="اپنا سوال یہاں لکھیں..."
          rows={1}
          disabled={isLoading}
        />
        <button 
          onClick={isLoading ? handleStop : handleSend}
          className={isLoading ? 'stop-button' : 'send-button'}
          style={{
            backgroundColor: isLoading ? '#ff4444' : '#4a90e2',
            color: 'white',
            padding: '12px 24px',
            border: 'none',
            borderRadius: '20px',
            cursor: 'pointer',
            fontSize: '16px',
            transition: 'all 0.2s ease',
            minWidth: '100px',
            opacity: 1,
            pointerEvents: 'auto'
          }}
        >
          {isLoading ? 'روکیں' : 'بھیجیں'}
        </button>
      </div>
    </div>
  );
};

export default StoryChat; 