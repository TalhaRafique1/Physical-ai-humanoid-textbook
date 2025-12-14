import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TextbookGenerationPage from './pages/TextbookGenerationPage';
import ExportPage from './pages/ExportPage';
import ChatbotPage from './pages/Chatbot/ChatbotPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Textbook Generation System</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<TextbookGenerationPage />} />
            <Route path="/generate" element={<TextbookGenerationPage />} />
            <Route path="/export" element={<ExportPage />} />
            <Route path="/chatbot" element={<ChatbotPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;