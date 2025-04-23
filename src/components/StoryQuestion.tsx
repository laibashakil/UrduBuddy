import React, { useState } from 'react';
import './StoryQuestion.css';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface StoryQuestionProps {
    storyId: string;
    storyContent: string;
}

// Common questions in Urdu
const commonQuestions = [
    "کہانی کا خلاصہ بتائیں",
    "کہانی کا سبق کیا ہے؟",
    "کہانی کے اہم کردار کون ہیں؟",
    "کہانی کا اختتام کیسے ہوا؟"
];

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const StoryQuestion: React.FC<StoryQuestionProps> = ({ storyId, storyContent }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleQuestionClick = (question: string) => {
        setInput(question);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await fetch(`${API_BASE_URL}/api/stories/${storyId}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: userMessage,
                    context: storyContent
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (!data.success) {
                throw new Error(data.error || 'Failed to get response from server');
            }
            
            setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } catch (error) {
            console.error('Error sending message:', error);
            setMessages(prev => [...prev, { 
                role: 'assistant', 
                content: 'Sorry, I encountered an error. Please try again.' 
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="story-chat">
            <div className="chat-header">
                <h2>کہانی یا نظم سے سوالات پوچھیں</h2>
                <p className="language-hint">آپ انگریزی یااردو میں سوال پوچھ سکتے ہیں۔</p>
            </div>
            
            <div className="common-questions">
                {commonQuestions.map((question, index) => (
                    <button
                        key={index}
                        className="question-button"
                        onClick={() => handleQuestionClick(question)}
                    >
                        {question}
                    </button>
                ))}
            </div>

            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.role}`}>
                        <div className="message-content">
                            {message.content}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message assistant">
                        <div className="message-content">
                            <span className="typing-indicator">...</span>
                        </div>
                    </div>
                )}
            </div>

            <form onSubmit={handleSubmit} className="chat-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="اپنا سوال یہاں ٹائپ کریں"
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading}>
                    بھیجیں
                </button>
            </form>
        </div>
    );
};

export default StoryQuestion; 