# Urdu Buddy - Interactive Urdu Learning App for Children

Urdu Buddy is an interactive application designed to help children learn Urdu through stories and poems. The app features:

- Age-appropriate stories and poems in Urdu
- Interactive question-answering about the content
- Automatic story extraction from PDF books
- Support for both stories and poems

## Setup and Installation

### Requirements
- Python 3.8+
- Node.js 14+
- npm 6+

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/urdu-buddy.git
cd urdu-buddy
```

2. Install backend dependencies:
```
pip install -r requirements.txt
```

3. Install frontend dependencies:
```
npm install
```

## Extracting Stories from PDF Books

Before using the app, you need to extract stories from your Urdu children's books (PDF format). The app comes with a batch extraction tool that can identify and separate individual stories and poems from PDF books.

### To extract stories from a PDF book:

```
python src/batch_extract_stories.py path/to/your/book.pdf
```

### Advanced options:

```
python src/batch_extract_stories.py path/to/your/book.pdf --output-dir data/stories --default-age 5-8
```

- `--output-dir`: Sets the output directory for the extracted stories (default: data/stories)
- `--default-age`: Sets the default age group when detection fails (default: 5-8)

The extractor will:
1. Read the PDF file
2. Identify individual stories and poems
3. Categorize them by type (story or poem)
4. Analyze and assign appropriate age groups
5. Save each as a JSON file in the data/stories directory, organized by age group

## Running the Application

To run the application in development mode:

```
npm run dev
```

This will start both the React frontend and Flask backend.

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Using the App

1. **Browse Stories**: The home page shows all available stories and poems organized by age group.
2. **Read Stories**: Click on any story to read it in its original Urdu format.
3. **Ask Questions**: While reading a story, you can ask questions about it in English or Roman Urdu. The application will provide answers in Urdu.

## App Architecture

- **Frontend**: React.js with TypeScript
- **Backend**: Flask API
- **RAG System**: 
  - Sentence Transformers for multilingual embeddings
  - FAISS for efficient similarity search
  - Context-aware question answering
- **PDF Processing**: Automatically extracts and categorizes stories from PDF books

## Technology Stack

- **Frontend**: React, TypeScript, React Router
- **Backend**: Flask, Python
- **RAG Components**:
  - Sentence Transformers (all-MiniLM-L6-v2)
  - FAISS for vector similarity search
  - Custom text chunking and embedding generation
- **PDF Extraction**: PyPDF2, pdfplumber

## Features

- **Smart Text Processing**:
  - Intelligent text chunking for Urdu content
  - Sentence-level relevance scoring
  - Context-aware answer generation
- **Multilingual Support**:
  - Urdu text processing
  - English/Roman Urdu question support
  - Urdu answer generation

## License

This project is licensed under the MIT License - see the LICENSE file for details.
