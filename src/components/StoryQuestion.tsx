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
    "کہانی کا عنوان کیا ہے؟",
    "کہانی سے کیا سبق ملتا ہے؟",
    "کہانی کے کردار کون کون ہیں؟",
    "کہانی کا پیغام کیا ہے؟",
    "کہانی کا خلاصہ کیا ہے؟",
    "کہانی کے مشکل الفاظ کون سے ہیں؟"
];

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const StoryQuestion: React.FC<StoryQuestionProps> = ({ storyId, storyContent }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [abortController, setAbortController] = useState<AbortController | null>(null);

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

        // Create new AbortController for this request
        const controller = new AbortController();
        setAbortController(controller);

        // Add minimum loading time
        const startTime = Date.now();
        const minLoadingTime = 1000; // 1 second minimum loading time

        try {
            // Clean up story_id to remove 'root/' prefix if present
            const cleanStoryId = storyId.replace('root/', '');
            
            const response = await fetch(`${API_BASE_URL}/api/stories/${cleanStoryId}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    message: userMessage,
                    story_id: cleanStoryId
                }),
                signal: controller.signal
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Calculate remaining time to ensure minimum loading time
            const elapsedTime = Date.now() - startTime;
            const remainingTime = Math.max(0, minLoadingTime - elapsedTime);
            
            // Wait for remaining time if needed
            if (remainingTime > 0) {
                await new Promise(resolve => setTimeout(resolve, remainingTime));
            }
            
            if (!data.success) {
                if (data.error === 'Could not find the requested information in the story') {
                    setMessages(prev => [...prev, { 
                        role: 'assistant', 
                        content: 'کہانی میں یہ معلومات موجود نہیں ہیں۔' 
                    }]);
                } else {
                    throw new Error(data.error || 'Failed to get response from server');
                }
            } else {
                setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
            }
        } catch (error: any) {
            if (error.name === 'AbortError') {
                setMessages(prev => [...prev, { 
                    role: 'assistant', 
                    content: 'جواب روک دیا گیا۔' 
                }]);
            } else {
                console.error('Error sending message:', error);
                setMessages(prev => [...prev, { 
                    role: 'assistant', 
                    content: 'معذرت، میں اس وقت سوالات کا جواب نہیں دے سکتا۔ براہ کرم دوبارہ کوشش کریں۔' 
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

    return (
        <div className="story-chat">
            <div className="chat-header">
                <h2>کہانی سے سوالات پوچھیں</h2>
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
                <button 
                    type="button"
                    onClick={isLoading ? handleStop : handleSubmit}
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
            </form>
        </div>
    );
};

export default StoryQuestion; 