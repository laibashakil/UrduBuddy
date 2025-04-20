import React, { useState, useRef, useEffect } from 'react';
import './StoryQuestion.css';

interface Message {
    role: 'user' | 'assistant';
    content: string;
}

interface StoryQuestionProps {
    storyId: string;
    storyContent: string;
}

// Define the API base URL
const API_BASE_URL = 'http://localhost:5000';

const StoryQuestion: React.FC<StoryQuestionProps> = ({ storyId, storyContent }) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = input.trim();
        setInput('');
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            // Use the full URL for the Flask server
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

            const data = await response.json();
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
                <h2>کہانی کے بارے میں بات کریں</h2>
                <p className="language-hint">آپ انگریزی یا رومن اردو میں سوال پوچھ سکتے ہیں، جواب اردو میں دیا جائے گا۔</p>
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
                <div ref={messagesEndRef} />
            </div>
            <form onSubmit={handleSubmit} className="chat-input">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="انگریزی یا رومن اردو میں اپنا پیغام ٹائپ کریں..."
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