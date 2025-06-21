import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useParams } from 'react-router-dom';
import './App.css';
import './styles/urdu.css';
import StoryLibrary from './components/StoryLibrary';
import StoryReader from './components/StoryReader';
import QuizLibrary from './components/QuizLibrary';
import Quiz from './components/Quiz';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <Link to="/" className="app-title">
            <div className="logo-container">
              <div className="logo-icon">📚</div>
              <h1>Urdu Buddy</h1>
            </div>
          </Link>
          <nav className="nav-links">
            <Link to="/" className="nav-link">Home</Link>
            <Link to="/stories" className="nav-link">Stories</Link>
            <Link to="/quizzes" className="nav-link">Quizzes</Link>
          </nav>
        </header>
        
        <main className="App-main">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/stories" element={<StoryLibrary />} />
            <Route path="/story/:storyId" element={<StoryReaderWrapper />} />
            <Route path="/story/root/:storyId" element={<StoryReaderWrapper />} />
            <Route path="/quizzes" element={<QuizLibrary />} />
            <Route path="/quiz/:storyId" element={<QuizWrapper />} />
            <Route path="/quiz/root/:storyId" element={<QuizWrapper />} />
          </Routes>
        </main>
        
        <footer className="App-footer">
          <div className="footer-content">
            <div className="footer-section">
              <h3>Urdu Buddy</h3>
              <p>Interactive Urdu language learning platform for kids</p>
            </div>
            <div className="footer-section">
              <h4>Features</h4>
              <ul>
                <li>Interactive Stories</li>
                <li>RAG-Powered Q&A</li>
                <li>Story Quizzes</li>
                <li>Vocabulary Building</li>
              </ul>
            </div>
            <div className="footer-section">
              <h4>Quick Links</h4>
              <ul>
                <li><Link to="/stories">Explore Stories</Link></li>
                <li><Link to="/quizzes">Take Quizzes</Link></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>&copy; 2024 Urdu Buddy. Learn Urdu through interactive stories.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

function HomePage() {
  return (
    <div className="home-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1 className="hero-title">
              Learn Urdu Through
              <span className="highlight"> Interactive Stories</span>
            </h1>
            <p className="hero-subtitle">
              Discover the beauty of Urdu language with engaging stories, intelligent Q&A, 
              and interactive quizzes designed for young learners.
            </p>
            <div className="hero-buttons">
              <Link to="/stories" className="cta-button primary">
                <span className="button-icon">📖</span>
                Explore Stories
              </Link>
              <Link to="/quizzes" className="cta-button secondary">
                <span className="button-icon">🧠</span>
                Take Quizzes
              </Link>
            </div>
          </div>
          <div className="hero-visual">
            <div className="floating-card card-1">
              <div className="card-icon">📚</div>
              <p>Interactive Stories</p>
            </div>
            <div className="floating-card card-2">
              <div className="card-icon">🤖</div>
              <p>AI-Powered Q&A</p>
            </div>
            <div className="floating-card card-3">
              <div className="card-icon">🎯</div>
              <p>Smart Quizzes</p>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="container">
          <h2 className="section-title">Why Choose Urdu Buddy?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📖</div>
              <h3>Rich Story Collection</h3>
              <p>Access a curated collection of age-appropriate Urdu stories with beautiful illustrations and engaging narratives.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>RAG-Powered Q&A</h3>
              <p>Ask questions about stories and get intelligent, contextually relevant answers using advanced AI technology.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h3>Interactive Quizzes</h3>
              <p>Test your understanding with interactive flashcards and quizzes based on story content and vocabulary.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💡</div>
              <h3>Vocabulary Building</h3>
              <p>Expand your Urdu vocabulary with definitions and examples for difficult words in each story.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎨</div>
              <h3>Beautiful Typography</h3>
              <p>Experience authentic Urdu with our custom Noto Nastaliq font for the most beautiful text rendering.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🚀</div>
              <h3>Fast & Reliable</h3>
              <p>Built with modern technology for fast loading times and smooth user experience across all devices.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">10+</div>
              <div className="stat-label">Interactive Stories</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">50+</div>
              <div className="stat-label">Quiz Questions</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">100+</div>
              <div className="stat-label">Vocabulary Words</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">AI Assistant</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Ready to Start Your Urdu Learning Journey?</h2>
            <p>Join thousands of learners who are discovering the beauty of Urdu through our interactive platform.</p>
            <div className="cta-buttons">
              <Link to="/stories" className="cta-button primary large">
                Start Reading Stories
              </Link>
              <Link to="/quizzes" className="cta-button secondary large">
                Try a Quiz
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

// Wrapper to extract the storyId parameter from the URL using useParams
function StoryReaderWrapper() {
  const params = useParams<{ storyId: string }>();
  const storyId = params.storyId;
  
  console.log('StoryReaderWrapper - storyId from params:', storyId);
  
  return <StoryReader storyId={storyId || ''} />;
}

// Wrapper to extract the storyId parameter for the Quiz component
function QuizWrapper() {
  const params = useParams<{ storyId: string }>();
  const storyId = params.storyId;
  
  console.log('QuizWrapper - storyId from params:', storyId);
  
  return <Quiz storyId={storyId || ''} />;
}

export default App; 