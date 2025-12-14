import axios, { AxiosResponse } from 'axios';
import { Textbook } from '../../../types/textbook';

// Base API URL - in a real application, this would be configured via environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth tokens if needed
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

/**
 * Interface for chatbot query response
 */
interface ChatbotQueryResponse {
  textbook_id: string;
  question: string;
  answer: string;
  sources: string[];
  confidence: number;
  timestamp: string;
}

/**
 * Interface for indexing response
 */
interface IndexTextbookResponse {
  textbook_id: string;
  status: string;
  message: string;
  chunk_count: number;
}

/**
 * Interface for textbook info response
 */
interface TextbookInfoResponse {
  id: string;
  title: string;
  description: string;
  target_audience: string;
  content_depth: string;
  chapters: number;
  indexed_at: string;
  chunk_count: number;
}

/**
 * API service for RAG chatbot functionality
 */
export const chatbotApi = {
  /**
   * Query the textbook content using the RAG chatbot
   */
  queryTextbook: async (textbookId: string, question: string): Promise<ChatbotQueryResponse> => {
    try {
      const response: AxiosResponse<ChatbotQueryResponse> = await apiClient.post(
        '/rag/query',
        {
          textbook_id: textbookId,
          question: question,
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error querying textbook:', error);
      throw error;
    }
  },

  /**
   * Index a textbook for RAG chatbot queries
   */
  indexTextbook: async (textbookId: string): Promise<IndexTextbookResponse> => {
    try {
      const response: AxiosResponse<IndexTextbookResponse> = await apiClient.post(
        '/rag/index',
        {
          textbook_id: textbookId,
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error indexing textbook:', error);
      throw error;
    }
  },

  /**
   * Get information about a textbook in the RAG index
   */
  getTextbookInfo: async (textbookId: string): Promise<TextbookInfoResponse> => {
    try {
      const response: AxiosResponse<TextbookInfoResponse> = await apiClient.get(
        `/rag/info/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting textbook info:', error);
      throw error;
    }
  },

  /**
   * List all indexed textbooks
   */
  listIndexedTextbooks: async (): Promise<TextbookInfoResponse[]> => {
    try {
      const response: AxiosResponse<TextbookInfoResponse[]> = await apiClient.get(
        '/rag/indexed'
      );
      return response.data;
    } catch (error) {
      console.error('Error listing indexed textbooks:', error);
      throw error;
    }
  },

  /**
   * Remove a textbook from the RAG index
   */
  removeTextbook: async (textbookId: string): Promise<{ textbook_id: string; status: string; message: string }> => {
    try {
      const response = await apiClient.delete(`/rag/remove/${textbookId}`);
      return response.data;
    } catch (error) {
      console.error('Error removing textbook from index:', error);
      throw error;
    }
  },

  /**
   * Validate a question before sending it to the chatbot
   */
  validateQuestion: async (question: string): Promise<{ valid: boolean; message: string }> => {
    try {
      const response = await apiClient.post('/rag/validate-question', {
        question: question,
      });
      return response.data;
    } catch (error) {
      console.error('Error validating question:', error);
      throw error;
    }
  },
};

export default chatbotApi;