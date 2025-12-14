import React, { useState, useEffect } from 'react';
import styles from './ChatWidget.module.css';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  // Note: We're not using useColorMode here to avoid context issues during SSR
  // The CSS will handle light/dark mode automatically

  // Add a sample welcome message when the chat opens
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      setMessages([
        {
          id: 'welcome',
          text: 'Hello! I\'m your AI assistant for this textbook. Ask me any questions about the content!',
          sender: 'bot',
          timestamp: new Date()
        }
      ]);
    }
  }, [isOpen, messages.length]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // In a real implementation, this would call the backend RAG API
      // For now, we'll simulate a response based on the input
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate network delay

      // Generate a response based on the user's input
      let responseText = "I'm an AI assistant trained on this textbook. ";

      if (inputValue.toLowerCase().includes('physical ai')) {
        responseText += "Physical AI refers to artificial intelligence systems that interact with and operate in the physical world, integrating sensing, computation, and actuation. Unlike traditional AI that operates in digital environments, Physical AI must deal with real-time constraints, uncertainty, and safety considerations.";
      } else if (inputValue.toLowerCase().includes('humanoid') || inputValue.toLowerCase().includes('robot')) {
        responseText += "Humanoid robots are designed with human-like characteristics to facilitate interaction with humans. They face unique challenges like bipedal locomotion and safe human-robot interaction, but offer benefits in terms of natural communication and environment compatibility.";
      } else if (inputValue.toLowerCase().includes('chapter') || inputValue.toLowerCase().includes('content')) {
        responseText += "This textbook covers Physical AI and Humanoid Robotics in 6-8 chapters. The content includes fundamentals of Physical AI, robotics basics, motion planning, humanoid design, applications, and future perspectives.";
      } else {
        responseText += "Based on the textbook content, Physical AI represents a paradigm shift where computational intelligence is tightly integrated with physical systems. It differs from traditional AI by operating in real-time, dealing with uncertainty, and having physical consequences for its actions.";
      }

      const botMessage = {
        id: Date.now() + 1,
        text: responseText,
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (err) {
      setError('Sorry, I encountered an error processing your question. Please try again.');
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your question. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend(e);
    }
  };

  return (
    <div className={styles.chatContainer}>
      {/* Chat Button */}
      {!isOpen && (
        <button
          className={styles.chatButton}
          onClick={toggleChat}
          aria-label="Open AI assistant chat"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={styles.icon}>
            <path d="M4.913 2.658C7.199 1.786 9.675 1.25 12.333 1.25c2.658 0 5.134.536 7.413 1.408 2.363.912 4.453 2.273 6.144 4.038 1.69 1.765 2.93 3.97 3.645 6.455.714 2.485.89 5.13.524 7.742-.365 2.613-1.215 5.04-2.492 7.13-1.277 2.09-2.957 3.79-4.938 4.938a16.702 16.702 0 01-7.13.525c-2.612-.365-5.038-1.215-7.455-2.492-2.417-1.277-4.326-2.957-5.72-4.938C2.06 17.86 1.21 15.433.845 12.82.48 10.208.656 7.563 1.37 5.077c.715-2.485 2.025-4.69 3.543-6.419zm4.26 15.384a1 1 0 10-1.937-.518c.218.817.645 1.584 1.243 2.232.598.648 1.346 1.148 2.214 1.46.868.313 1.82.434 2.802.35-.982.084-1.934-.037-2.802-.35a4.848 4.848 0 01-2.214-1.46c-.598-.648-1.025-1.415-1.243-2.232zM15.5 14a1.5 1.5 0 100-3 1.5 1.5 0 000 3z" />
          </svg>
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>AI Textbook Assistant</h3>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className={styles.chatMessages}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${styles[message.sender]}`}
              >
                <div className={styles.messageContent}>
                  {message.text}
                </div>
                <div className={styles.timestamp}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typingIndicator}>
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={`${styles.messageContent} ${styles.error}`}>
                  {error}
                </div>
              </div>
            )}
          </div>

          <form onSubmit={handleSend} className={styles.chatInputForm}>
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a question about the textbook content..."
              className={styles.chatInput}
              rows={2}
              aria-label="Type your question for the AI assistant"
            />
            <button
              type="submit"
              className={styles.sendButton}
              disabled={!inputValue.trim() || isLoading}
              aria-label="Send message"
            >
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className={styles.sendIcon}>
                <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
              </svg>
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ChatWidget;