import React, { useState, useEffect, useRef } from 'react';
import { Textbook } from '../../types/textbook';
import { chatbotApi } from '../../services/api/chatbotApi';

interface RAGChatbotProps {
  textbook?: Textbook;
  textbookId?: string;
}

interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  sources?: string[];
  confidence?: number;
}

const RAGChatbot: React.FC<RAGChatbotProps> = ({ textbook, textbookId: propTextbookId }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  // Use the textbookId from props or from the textbook object
  const textbookId = propTextbookId || textbook?.id;

  useEffect(() => {
    // Initialize with a welcome message
    setMessages([
      {
        id: 'welcome-' + Date.now(),
        text: textbook
          ? `Hello! I'm your RAG chatbot for "${textbook.title}". Ask me questions about the textbook content!`
          : 'Hello! I\'m your RAG chatbot. Please provide a textbook to start chatting!',
        sender: 'bot',
        timestamp: new Date(),
      }
    ]);
  }, [textbook]);

  useEffect(() => {
    // Scroll to bottom of messages
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // Clean up WebSocket on component unmount
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [ws]);

  const handleSendMessage = async () => {
    if (!inputText.trim() || !textbookId) {
      return;
    }

    // Add user message to chat
    const userMessage: ChatMessage = {
      id: 'user-' + Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setError(null);

    try {
      // Use the chatbot API to get response
      const response = await chatbotApi.queryTextbook(textbookId, inputText);

      const botMessage: ChatMessage = {
        id: 'bot-' + Date.now(),
        text: response.answer,
        sender: 'bot',
        timestamp: new Date(),
        sources: response.sources,
        confidence: response.confidence,
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      console.error('Error getting chatbot response:', err);
      setError('Failed to get response from chatbot. Please try again.');

      const errorMessage: ChatMessage = {
        id: 'error-' + Date.now(),
        text: 'Sorry, I encountered an error processing your question. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleIndexTextbook = async () => {
    if (!textbookId) {
      setError('No textbook selected');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);

      const result = await chatbotApi.indexTextbook(textbookId);
      console.log('Textbook indexed:', result);

      // Add a system message
      const systemMessage: ChatMessage = {
        id: 'system-' + Date.now(),
        text: `Textbook "${textbook?.title || textbookId}" has been indexed for RAG chatbot. You can now ask questions about its content.`,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, systemMessage]);
    } catch (err) {
      console.error('Error indexing textbook:', err);
      setError('Failed to index textbook for chatbot. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="rag-chatbot">
      <div className="chatbot-header">
        <h3>RAG Chatbot</h3>
        <div className="chatbot-status">
          <span className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}></span>
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {!textbookId && (
        <div className="no-textbook-warning">
          <p>Please select a textbook to enable chatbot functionality.</p>
        </div>
      )}

      {textbookId && !isConnected && (
        <div className="index-prompt">
          <p>This textbook needs to be indexed for the chatbot.</p>
          <button onClick={handleIndexTextbook} disabled={isLoading}>
            {isLoading ? 'Indexing...' : 'Index Textbook for Chatbot'}
          </button>
        </div>
      )}

      <div className="chat-messages">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender}-message`}
            aria-label={`${message.sender} message: ${message.text}`}
          >
            <div className="message-header">
              <span className="sender-name">{message.sender === 'user' ? 'You' : 'Chatbot'}</span>
              <span className="timestamp">
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </span>
            </div>
            <div className="message-content">
              {message.text}
              {message.confidence !== undefined && message.confidence < 0.5 && (
                <div className="low-confidence-notice">
                  <small>This answer has low confidence. The information may not be directly from the textbook.</small>
                </div>
              )}
              {message.sources && message.sources.length > 0 && (
                <div className="sources">
                  <details>
                    <summary>Sources in textbook</summary>
                    <ul>
                      {message.sources.slice(0, 2).map((source, index) => (
                        <li key={index} className="source-snippet">
                          {source.substring(0, 100)}...
                        </li>
                      ))}
                    </ul>
                  </details>
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot-message">
            <div className="message-header">
              <span className="sender-name">Chatbot</span>
            </div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={textbookId ? "Ask a question about the textbook..." : "Select a textbook first..."}
          disabled={!textbookId || isLoading}
          rows={3}
          aria-label="Type your question for the chatbot"
        />
        <button
          onClick={handleSendMessage}
          disabled={!inputText.trim() || !textbookId || isLoading}
          aria-label="Send message to chatbot"
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default RAGChatbot;