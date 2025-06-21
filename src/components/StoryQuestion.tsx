import React, { useState, useEffect, useRef } from 'react';
import './StoryQuestion.css';
import TypingIndicator from './TypingIndicator';

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
    const chatMessagesRef = useRef<HTMLDivElement | null>(null);

    // Auto-scroll to the bottom when messages change
    useEffect(() => {
        if (chatMessagesRef.current) {
            chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
        }
    }, [messages]);

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

        // Add a temporary "thinking" message
        const thinkingMessage = { role: 'assistant' as const, content: '...' };
        setMessages(prev => [...prev, thinkingMessage]);

        // Delay for 2 seconds to simulate thinking
        setTimeout(async () => {
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
                
                // Remove "thinking" message and add the real response
                setMessages(prev => {
                    const filtered = prev.filter(m => m.content !== '...');
                    if (!data.success) {
                        return [...filtered, { 
                            role: 'assistant', 
                            content: data.error || 'معذرت، میں اس وقت سوالات کا جواب نہیں دے سکتا۔ براہ کرم دوبارہ کوشش کریں۔' 
                        }];
                    } else {
                        return [...filtered, { role: 'assistant', content: data.response }];
                    }
                });
            } catch (error: any) {
                if (error.name === 'AbortError') {
                    setMessages(prev => {
                        const filtered = prev.filter(m => m.content !== '...');
                        return [...filtered, { 
                            role: 'assistant', 
                            content: 'جواب روک دیا گیا۔' 
                        }];
                    });
                } else {
                    console.error('Error sending message:', error);
                    setMessages(prev => {
                        const filtered = prev.filter(m => m.content !== '...');
                        return [...filtered, { 
                            role: 'assistant', 
                            content: 'معذرت، میں اس وقت سوالات کا جواب نہیں دے سکتا۔ براہ کرم دوبارہ کوشش کریں۔' 
                        }];
                    });
                }
            } finally {
                setIsLoading(false);
                setAbortController(null);
            }
        }, 2000); // 2-second delay
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

            <div className="chat-messages" ref={chatMessagesRef}>
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.role}`}>
                        <div className={`message-content ${message.role === 'user' ? 'urdu' : ''}`}>
                            {message.content === '...' ? <TypingIndicator /> : message.content}
                        </div>
                    </div>
                ))}
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