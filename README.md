# Urdu Buddy

Urdu Buddy is an interactive application for learning Urdu through stories, poems, and quizzes. It features a RAG (Retrieval-Augmented Generation) system for answering questions about stories.

## Features

- Interactive Urdu stories and poems
- AI-powered chat interface for asking questions about stories
- Story quizzes to test comprehension
- Vocabulary and alphabet learning tools

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm (Node Package Manager)

## Installation

### Backend Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/urdu-buddy.git
   cd urdu-buddy
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd src/frontend
   ```

2. Install npm dependencies:
   ```
   npm install
   ```

## Running the Application

### Start the Backend Server

1. From the project root directory, run:
   ```
   python src/flask_server.py
   ```

   This will start the Flask server on http://localhost:5000

### Start the Frontend Development Server

1. In a new terminal, navigate to the frontend directory:
   ```
   cd src/frontend
   ```

2. Start the development server:
   ```
   npm start
   ```

   This will start the React development server on http://localhost:3000

3. Open your browser and navigate to http://localhost:3000 to use the application

## Usage

- Browse stories and poems in the Stories Library
- Click on a story to read it
- Use the chat interface at the bottom of each story to ask questions
- Questions can be asked in English or Roman Urdu
- The system will respond in Urdu script

## Troubleshooting

- If you encounter a 404 error when accessing stories, make sure both the backend and frontend servers are running
- If the chat interface doesn't respond, check that the Flask server is running on port 5000
- For any other issues, check the console logs in your browser's developer tools

## License

[MIT License](LICENSE)
