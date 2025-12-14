import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import RAGChatbot from '../../components/Chatbot/RAGChatbot';
import { textbookGenerationApi } from '../../services/api/textbookGenerationApi';
import { Textbook } from '../../types/textbook';

const ChatbotPage: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [textbookId, setTextbookId] = useState<string>('');
  const [textbook, setTextbook] = useState<Textbook | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Get textbook ID from URL params
    const id = searchParams.get('textbookId') || '';
    if (id) {
      setTextbookId(id);
      loadTextbook(id);
    } else {
      // If no textbook ID is provided, we can still show the chatbot component
      // but it will indicate that no textbook is selected
      setLoading(false);
    }
  }, [searchParams]);

  const loadTextbook = async (id: string) => {
    try {
      setLoading(true);
      setError(null);

      const textbookData = await textbookGenerationApi.getTextbook(id);
      setTextbook(textbookData);
    } catch (err) {
      console.error('Error loading textbook:', err);
      setError('Failed to load textbook information. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="chatbot-page">
        <h2>RAG Chatbot</h2>
        <p>Loading textbook information...</p>
      </div>
    );
  }

  return (
    <div className="chatbot-page">
      <h2>RAG Chatbot</h2>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={() => window.history.back()}>Go Back</button>
        </div>
      )}

      {textbook && (
        <div className="textbook-info">
          <h3>Chatting about: {textbook.title}</h3>
          <p><strong>Description:</strong> {textbook.description}</p>
          <p><strong>Status:</strong> {textbook.status}</p>
          <p><strong>Chapters:</strong> {textbook.totalChapters}</p>
          <p><strong>Audience:</strong> {textbook.targetAudience}</p>
        </div>
      )}

      <div className="chatbot-container">
        <RAGChatbot textbook={textbook} textbookId={textbookId} />
      </div>

      <div className="chatbot-actions">
        <button onClick={() => window.location.href = '/'}>
          Back to Home
        </button>
        <button onClick={() => window.location.href = `/generate?textbookId=${textbookId}`}>
          Back to Textbook
        </button>
        <button onClick={() => window.location.href = `/export?textbookId=${textbookId}`}>
          Export Textbook
        </button>
      </div>
    </div>
  );
};

export default ChatbotPage;