import axios, { AxiosResponse } from 'axios';
import { Textbook } from '../../types/textbook';

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
 * API service for learning tools functionality
 */
export const learningToolsApi = {
  /**
   * Generate summary for a textbook
   */
  generateSummary: async (textbookId: string, length: string = 'medium'): Promise<any> => {
    try {
      const response = await apiClient.post(
        `/learning-tools/generate-summary/${textbookId}`,
        { length },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error generating summary:', error);
      throw error;
    }
  },

  /**
   * Generate quiz for a textbook
   */
  generateQuiz: async (textbookId: string, numQuestions: number = 10): Promise<any> => {
    try {
      const response = await apiClient.post(
        `/learning-tools/generate-quiz/${textbookId}`,
        { num_questions: numQuestions },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error generating quiz:', error);
      throw error;
    }
  },

  /**
   * Generate comprehensive learning materials for a textbook
   */
  generateLearningMaterials: async (textbookId: string): Promise<any> => {
    try {
      const response = await apiClient.post(
        `/learning-tools/generate-learning-materials/${textbookId}`,
        {},
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error generating learning materials:', error);
      throw error;
    }
  },

  /**
   * Generate learning materials for a specific chapter
   */
  generateChapterMaterials: async (textbookId: string, chapterNumber: number): Promise<any> => {
    try {
      const response = await apiClient.post(
        `/learning-tools/generate-chapter-materials/${textbookId}/${chapterNumber}`,
        {},
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error generating chapter materials:', error);
      throw error;
    }
  },

  /**
   * Check the health of the learning tools service
   */
  healthCheck: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/learning-tools/health');
      return response.data;
    } catch (error) {
      console.error('Error checking learning tools health:', error);
      throw error;
    }
  },
};

export default learningToolsApi;