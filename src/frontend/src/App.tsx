import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import StoryPage from './pages/StoryPage';
import StoryLibrary from './pages/StoryLibrary';

const App: React.FC = () => {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<StoryLibrary />} />
          <Route path="/story/:storyId" element={<StoryPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App; 