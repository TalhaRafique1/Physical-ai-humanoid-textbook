import React, { useState, useEffect } from 'react';
import { GenerationParams, Textbook, GenerationStatus, ProgressMessage } from '../types/textbook';
import GeneratorForm from '../components/TextbookGenerator/GeneratorForm';
import ProgressIndicator from '../components/TextbookGenerator/ProgressIndicator';
import { textbookGenerationApi } from '../services/api/textbookGenerationApi';

const TextbookGenerationPage: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<'form' | 'generating' | 'completed'>('form');
  const [generationParams, setGenerationParams] = useState<GenerationParams | null>(null);
  const [textbookId, setTextbookId] = useState<string | null>(null);
  const [progress, setProgress] = useState<number>(0);
  const [status, setStatus] = useState<string>('Ready to generate');
  const [generatedTextbook, setGeneratedTextbook] = useState<Textbook | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [ws, setWs] = useState<WebSocket | null>(null);

  const handleFormSubmit = async (params: GenerationParams) => {
    setError(null);
    setGenerationParams(params);
    setCurrentStep('generating');

    try {
      // Call the API to start textbook generation
      const response = await textbookGenerationApi.generateTextbook(params);
      setTextbookId(response.textbookId);
      setStatus(response.message);

      // Set up WebSocket connection for progress updates
      const wsUrl = `ws://localhost:8000/api/textbook-generation/ws/progress/${response.textbookId}`;
      const websocket = new WebSocket(wsUrl);

      websocket.onopen = () => {
        console.log('WebSocket connected for progress updates');
        setWs(websocket);
      };

      websocket.onmessage = (event) => {
        const data: ProgressMessage = JSON.parse(event.data);
        setProgress(data.progress);
        setStatus(data.message);

        // If generation is completed, move to completed step
        if (data.status === 'completed') {
          setCurrentStep('completed');
          fetchGeneratedTextbook(response.textbookId);
          websocket.close();
        } else if (data.status === 'failed') {
          setError(data.message);
          setCurrentStep('form');
        }
      };

      websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        setError('Connection error. Progress updates unavailable.');
      };

      websocket.onclose = () => {
        console.log('WebSocket disconnected');
        setWs(null);
      };
    } catch (err) {
      console.error('Error starting textbook generation:', err);
      setError('Failed to start textbook generation. Please try again.');
      setCurrentStep('form');
    }
  };

  const fetchGeneratedTextbook = async (id: string) => {
    try {
      const textbook = await textbookGenerationApi.getTextbook(id);
      setGeneratedTextbook(textbook);
    } catch (err) {
      console.error('Error fetching textbook:', err);
      setError('Failed to fetch generated textbook.');
    }
  };

  const handleNewGeneration = () => {
    // Reset the form and start over
    setCurrentStep('form');
    setProgress(0);
    setStatus('Ready to generate');
    setGeneratedTextbook(null);
    setTextbookId(null);
    setError(null);

    // Close WebSocket if it's open
    if (ws) {
      ws.close();
      setWs(null);
    }
  };

  useEffect(() => {
    // Clean up WebSocket on component unmount
    return () => {
      if (ws) {
        ws.close();
      }
    };
  }, [ws]);

  return (
    <div className="textbook-generation-page">
      <h2>Textbook Generation</h2>

      {error && (
        <div className="error-message">
          <p>Error: {error}</p>
          <button onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      {currentStep === 'form' && (
        <div className="generation-form-section">
          <h3>Generate New Textbook</h3>
          <p>Fill in the details below to generate a customized textbook based on your requirements.</p>
          <GeneratorForm onSubmit={handleFormSubmit} />
        </div>
      )}

      {(currentStep === 'generating' || currentStep === 'completed') && (
        <div className="generation-progress-section">
          <ProgressIndicator
            progress={progress}
            status={status}
            textbookId={textbookId || undefined}
          />
        </div>
      )}

      {currentStep === 'completed' && generatedTextbook && (
        <div className="generation-completed-section">
          <h3>Textbook Generated Successfully!</h3>

          <div className="textbook-summary">
            <h4>Textbook Details:</h4>
            <p><strong>Title:</strong> {generatedTextbook.title}</p>
            <p><strong>Description:</strong> {generatedTextbook.description}</p>
            <p><strong>Status:</strong> {generatedTextbook.status}</p>
            <p><strong>Total Chapters:</strong> {generatedTextbook.totalChapters}</p>
            <p><strong>Target Audience:</strong> {generatedTextbook.targetAudience}</p>
            <p><strong>Content Depth:</strong> {generatedTextbook.contentDepth}</p>
            <p><strong>Writing Style:</strong> {generatedTextbook.writingStyle}</p>
          </div>

          {generatedTextbook.generatedContent && (
            <div className="generated-content-preview">
              <h4>Content Preview:</h4>
              <div className="preview-content">
                {generatedTextbook.generatedContent.substring(0, 500)}
                {generatedTextbook.generatedContent.length > 500 ? '...' : ''}
              </div>
            </div>
          )}

          <div className="generation-actions">
            <button onClick={() => window.location.href = `/export?textbookId=${generatedTextbook.id}`}>
              Export Textbook
            </button>
            <button onClick={handleNewGeneration}>
              Generate Another Textbook
            </button>
          </div>
        </div>
      )}

      {currentStep === 'completed' && !generatedTextbook && (
        <div className="loading-textbook">
          <p>Loading textbook details...</p>
        </div>
      )}
    </div>
  );
};

export default TextbookGenerationPage;