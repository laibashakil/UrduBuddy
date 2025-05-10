# Urdu Buddy - Interactive Urdu Language Learning Platform for kids

A modern web application for learning Urdu through interactive stories, vocabulary, and language exercises. Built with React, TypeScript, and Python, Urdu Buddy provides an engaging platform for Urdu language learners of all ages.

## 🌟 Features

- **Interactive Stories**: Access a collection of age-appropriate Urdu stories with chatbox
- **RAG-Powered Q&A**: Ask questions about stories and get intelligent responses using Retrieval-Augmented Generation
- **Interactive Quizzes**: Test your understanding of stories with structured flashcards based on story metadata
- **RTL Support**: Full support for Right-to-Left text rendering
- **Custom Urdu Font**: Uses Noto Nastaliq Urdu for authentic Urdu typography

## 🤖 RAG-Powered Q&A System

The Q&A system uses a sophisticated three-tier approach to provide accurate and contextually relevant answers to questions about Urdu stories.

### How It Works

1. **Direct Answer from JSON Data**
   - For common question types, answers are retrieved directly from story metadata
   - Supported question types:
     - Title questions (کہانی کا عنوان کیا ہے؟)
     - Lesson questions (کہانی سے کیا سبق ملتا ہے؟)
     - Character questions (کہانی کے کردار کون کون ہیں؟)
     - Moral questions (کہانی کا پیغام کیا ہے؟)
     - Summary questions (کہانی کا خلاصہ کیا ہے؟)
     - Difficult words questions (کہانی کے مشکل الفاظ کون سے ہیں؟)
   - Fastest response time as it bypasses the RAG pipeline
   - Ensures consistent answers for standard questions

2. **Sentence Completion**
   - Detects partial sentences and completes them
   - Uses exact matching to find the continuation
   - Preserves context and flow of the story
   - Ideal for interactive reading and learning
   - Handles both sentence starts and mid-sentence completions

3. **RAG Pipeline**
   - Used when direct answers and sentence completion aren't applicable
   - Process:
     1. **Text Chunking**: Splits stories into meaningful chunks
     2. **Embedding Generation**: Creates vector embeddings for questions and chunks
     3. **Vector Storage**: Uses ChromaDB for efficient storage
     4. **Context Retrieval**: Finds relevant story chunks
     5. **Response Generation**: Uses TinyLlama for answer generation
     6. **Response Validation**: Ensures answer quality and relevance

### Key Components

- **RAGHandler**: Main class managing the Q&A pipeline
- **StoryHandler**: Manages story data and metadata
- **Embedding Model**: Multilingual sentence transformer
- **Vector Database**: ChromaDB for efficient storage
- **Language Model**: TinyLlama for response generation

### Performance Optimizations

- Caching of embeddings and model instances
- Efficient chunking strategy
- Context overlap prevention
- Token limit management
- Response validation pipeline

### Error Handling

- Graceful fallback between answer methods
- Context not found handling
- Invalid response detection
- Model loading error recovery

## 📚 Interactive Quiz System

The quiz system provides an engaging way to test comprehension of Urdu stories through interactive flashcards generated from story metadata.

### How It Works

1. **Quiz Generation**
   - Uses predefined story metadata to generate questions
   - Creates questions and answers in Urdu
   - Maintains consistent question types across stories
   - Generates questions based on story elements

2. **Question Types**
   - Title questions (کہانی کا عنوان کیا ہے؟)
   - Lesson questions (کہانی سے کیا سبق ملتا ہے؟)
   - Character questions (کہانی کے کردار کون کون ہیں؟)
   - Summary questions (کہانی کا خلاصہ کیا ہے؟)
   - Moral questions (کہانی کا پیغام کیا ہے؟)
   - Vocabulary questions (مشکل الفاظ کے معنی)

3. **Flashcard Interface**
   - Interactive cards with questions on front
   - Answers revealed on click
   - Smooth flip animation
   - RTL support for Urdu text

4. **Features**
   - Consistent question format
   - Immediate feedback
   - Easy navigation
   - Mobile-responsive design
   - Offline functionality

### Key Components

- **Quiz Component**: Manages the quiz interface and state
- **Flashcard Component**: Handles individual question display
- **Story Metadata**: Powers question generation
- **Error Handling**: Ensures smooth user experience

### Usage

1. Navigate to the Quizzes section
2. Select a story to quiz on
3. View and interact with flashcards
4. Click cards to reveal answers
5. Test your understanding of the story

### Story JSON Structure

Each story JSON file contains the following fields used for quiz generation:
```json
{
    "title": "Story title in Urdu",
    "lesson": "Lesson from the story",
    "characters": [
        {
            "name": "Character name",
            "description": "Character description"
        }
    ],
    "summary": "Story summary",
    "moral": "Story moral",
    "difficult_words": [
        {
            "word": "Difficult word",
            "meaning": "Word meaning",
            "example": "Usage example"
        }
    ]
}
```

## 🚀 Tech Stack

### Frontend
- React 18
- TypeScript
- React Router
- Custom CSS with RTL support
- Noto Nastaliq Urdu font

### Backend
- Python Flask
- ChromaDB for vector storage
- Sentence Transformers for embeddings
- TinyLlama for language model
- NLTK for text processing

## 📋 Prerequisites

- Node.js (v16 or higher)
- Python 3.8 or higher
- pip (Python package manager)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/laibashakil/urdubuddy.git
cd urdubuddy
```

2. Install frontend dependencies:
```bash
npm install
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Download required models:
```bash
# Create models directory
mkdir models
# Download TinyLlama model
wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -O models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf
```

## 🚀 Running the Application

1. Start the development server:
```bash
python src/flask_server.py
```

2. Start the frontend
```bash
npm start
```

- Frontend: http://localhost:3000
- Backend: http://localhost:5000


## 🙏 Acknowledgments

- [Noto Nastaliq Urdu](https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu) for the beautiful Urdu font
- [TinyLlama](https://github.com/TinyLlama/TinyLlama) for the lightweight language model
- [ChromaDB](https://www.trychroma.com/) for vector storage
- [Sentence Transformers](https://www.sbert.net/) for text embeddings
