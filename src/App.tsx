import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams } from 'react-router-dom';
import './App.css';
import './styles/urdu.css';
import StoryLibrary from './components/StoryLibrary';
import StoryReader from './components/StoryReader';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Link to="/" className="app-title">
            <h1>Urdu Buddy</h1>
          </Link>
          <nav className="nav-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/stories" className="nav-link">Stories</Link>
          </nav>
        </header>
        
        <main className="App-main">
          <Routes>
            <Route path="/" element={
              <div className="home-container">
                <h1 className="home-title">Welcome to Urdu Buddy</h1>
                <div className="button-container">
                  <Link to="/ask" className="button ask-button">Ask About Stories</Link>
                  <Link to="/quizzes" className="button quiz-button">Story Quizzes</Link>
                  <Link to="/stories" className="button explore-button">Explore Stories</Link>
                </div>
              </div>
            } />
            <Route path="/stories" element={<StoryLibrary />} />
            <Route path="/story/root/:storyId" element={<StoryReaderWrapper />} />
          </Routes>
        </main>
        
        <footer className="App-footer">
          <p>Urdu Buddy - Learn Urdu through interactive stories</p>
        </footer>
      </div>
    </Router>
  );
}

// Wrapper to extract the storyId parameter from the URL using useParams
function StoryReaderWrapper() {
  const params = useParams<{ storyId: string }>();
  const storyId = params.storyId;
  
  console.log('StoryReaderWrapper - storyId from params:', storyId);
  
  return <StoryReader storyId={storyId || ''} />;
}

export default App; 