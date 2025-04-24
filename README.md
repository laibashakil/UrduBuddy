# Urdu Buddy

Urdu Buddy is an interactive application for learning Urdu through stories, poems, and quizzes. It features a sophisticated RAG (Retrieval-Augmented Generation) system for answering questions about stories, specifically designed for the Urdu Tutor Datathon.

## System Architecture

### LLM Configuration
- Primary Model: TinyLlama 1.1B (Q4_K_M quantized)
  - Parameters: 1.1B
  - Quantization: Q4_K_M (4-bit quantization)
  - Context Length: 512 tokens
  - Temperature: 0.2
  - Max New Tokens: 256
- Embedding Model: Multilingual MiniLM-L12-v2
  - Supports multiple languages including Urdu
  - Efficient for semantic search

### Cost-Effective Design
- Uses quantized models to reduce memory footprint
- Implements efficient context management
- Employs multiple validation layers to reduce API calls
- Caches embeddings and responses for better performance

## RAG Workflow

The system implements a sophisticated RAG (Retrieval-Augmented Generation) pipeline optimized for Urdu language processing:

### 1. Document Processing
- **Story Loading**
  - Loads Urdu stories from JSON files
  - Extracts metadata (title, lesson, characters, etc.)
  - Preserves story structure and formatting

- **Text Chunking**
  - Splits stories into sentence-level chunks
  - Preserves sentence boundaries and context
  - Maintains semantic coherence
  - Chunk size: 200 tokens with overlap handling

### 2. Embedding Generation
- **Multilingual Embeddings**
  - Uses sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
  - Generates embeddings for each chunk
  - Supports both Urdu and Roman Urdu text
  - Optimized for semantic similarity search

- **Vector Storage**
  - Stores embeddings in ChromaDB
  - Implements cosine similarity search
  - Maintains metadata for each chunk
  - Enables efficient retrieval

### 3. Query Processing
- **Question Analysis**
  - Detects question type (title, lesson, summary, etc.)
  - Extracts key terms and context
  - Handles both Urdu and Roman Urdu questions
  - Supports exact and semantic matching

- **Context Retrieval**
  - Performs semantic search using question embedding
  - Retrieves top-k relevant chunks (k=3)
  - Applies similarity threshold (0.5)
  - Handles context overlap

### 4. Response Generation
- **Prompt Construction**
  - System: "Answer based ONLY on this context. If unsure, say: 'کہانی میں ذکر نہیں۔'"
  - Context: Retrieved relevant chunks
  - Question: User's query
  - Format: Structured for TinyLlama

- **Response Generation**
  - Uses TinyLlama for text generation
  - Temperature: 0.2 for focused responses
  - Max tokens: 256
  - Enforces Urdu language output

### 5. Response Validation
- **Quality Checks**
  - Word overlap validation
  - Semantic similarity verification
  - Minimum length requirement (10 tokens)
  - Context relevance check

- **Hallucination Prevention**
  - Multiple validation layers
  - Fallback mechanisms
  - Clear "not found" responses
  - Error handling

### 6. Performance Optimization
- **Caching**
  - Caches embeddings for stories
  - Stores frequent responses
  - Reduces computation overhead
  - Improves response time

- **Resource Management**
  - Efficient memory usage
  - Token limit monitoring
  - Context window management
  - Error recovery

### 7. Evaluation Metrics
- **Response Quality**
  - Hallucination rate: 91.82%
  - Accuracy: 17.25%
  - Response length: 175 characters avg.
  - Error rate: 0%

- **Performance**
  - Load time: 7.51 seconds
  - Response time: 18.63 seconds avg.
  - Memory usage: 737.25 MB
  - Context retrieval: < 1 second

## Features

- Interactive Urdu stories and poems
- AI-powered chat interface for asking questions about stories
- Story quizzes to test comprehension
- Vocabulary and alphabet learning tools

## Question Answering Techniques

The system employs three sophisticated techniques to answer questions about stories:

1. **Exact Question Matching**
   - Handles predefined question patterns about story elements
   - Supports questions about:
     - Story title (کہانی کا عنوان کیا ہے؟)
     - Lesson/moral (کہانی سے کیا سبق ملتا ہے؟)
     - Characters (کہانی کے کردار کون کون ہیں؟)
     - Summary (کہانی کا خلاصہ کیا ہے؟)
     - Difficult words (کہانی کے مشکل الفاظ کون سے ہیں؟)
   - Provides direct, structured answers from story metadata

2. **RAG-based Dynamic Answering**
   - Uses Retrieval-Augmented Generation for general questions
   - Process:
     1. Converts question to embeddings using multilingual sentence transformer
     2. Retrieves relevant context from the story using semantic search
     3. Generates answer using TinyLlama model
     4. Validates response against context for relevance
   - Handles questions not covered by exact matching
   - Supports both Urdu and Roman Urdu questions

3. **Sentence Completion**
   - Helps users recall specific parts of stories
   - Features:
     - Completes partial sentences from stories
     - Matches text fragments to full sentences
     - Works with both story files and vector database
     - Preserves sentence context and meaning
   - Useful for finding specific story segments

## Hallucination Prevention

The system implements multiple layers of hallucination prevention:

1. **Response Validation**
   - Word overlap checking
   - Semantic similarity validation
   - Minimum response length requirements
   - Context relevance verification

2. **Context Management**
   - Strict context window limits
   - Sentence-level chunking
   - Overlap detection and removal
   - Token count monitoring

3. **Fallback Mechanisms**
   - Multiple validation layers
   - Graceful degradation
   - Clear "not found" responses
   - Error handling and recovery

## Performance Metrics

The system has been tested with the following performance results:

- **Model Loading**:
  - Load Time: 7.51 seconds
  - Memory Usage: 737.25 MB

- **Response Metrics**:
  - Average Response Time: 18.63 seconds
  - Average Response Length: 175 characters
  - Error Rate: 0%

- **Quality Metrics**:
  - Average Hallucination Level: 91.82%
  - Average Accuracy: 17.25%

- **Model Configuration**:
  - TinyLlama 1.1B (Q4_K_M quantized)
  - Context Length: 512 tokens
  - Max New Tokens: 256
  - Temperature: 0.2

- **Memory Requirements**:
  - TinyLlama Model: ~500MB (Q4_K_M quantized)
  - Embedding Model: ~100MB
  - Vector Database: ~50MB
  - Total: < 700MB

- **Context Management**:
  - Chunk Size: 200 tokens
  - Overlap Threshold: 0.2
  - Similarity Threshold: 0.5
  - Min Response Length: 10 tokens

- **Validation Mechanisms**:
  - Word overlap checking
  - Semantic similarity validation
  - Context relevance verification
  - Response length validation

Note: These metrics are based on testing with a representative dataset of Urdu stories and questions. The high hallucination rate and low accuracy indicate areas for improvement in the model's performance.

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm (Node Package Manager)
- 4GB RAM minimum
- 500MB free disk space

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/laibashakil/urdubuddy.git
   cd urdubuddy
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install npm dependencies:
   ```
   npm install
   ```

4. Download required models:
   ```
   python scripts/download_models.py
   ```

5. Start the backend server:
   ```
   python src/flask_server.py
   ```

6. Start the frontend development server:
   ```
   npm start
   ```

## Usage

- Browse stories and poems in the Stories Library
- Click on a story to read it
- Use the chat interface at the bottom of each story to ask questions
- Questions can be asked in English or Roman Urdu
- The system will respond in Urdu script

## Evaluation

The system has been evaluated on:
- Response accuracy
- Hallucination rates
- Response time
- Memory usage
- Cost efficiency

## Troubleshooting

- If you encounter a 404 error when accessing stories, make sure both the backend and frontend servers are running
- If the chat interface doesn't respond, check that the Flask server is running on port 5000
- For any other issues, check the console logs in your browser's developer tools

## License

[MIT License](LICENSE)
