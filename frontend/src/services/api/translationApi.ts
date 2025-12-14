import axios, { AxiosResponse } from 'axios';
import { Textbook } from '../../types/textbook';

// Base API URL - in a real application, this would be configured via environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 second timeout for translation operations
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
 * API service for translation functionality
 */
export const translationApi = {
  /**
   * Translate a textbook to the specified language
   */
  translateTextbook: async (textbookId: string, targetLanguage: string = 'ur'): Promise<any> => {
    try {
      const response = await apiClient.post(
        `/translation/translate/${textbookId}`,
        { target_language: targetLanguage },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error translating textbook:', error);
      throw error;
    }
  },

  /**
   * Translate a textbook to multiple languages
   */
  translateTextbookMultiple: async (textbookId: string, languages: string[]): Promise<any> => {
    try {
      const response = await apiClient.post(
        `/translation/translate/multiple/${textbookId}`,
        { languages },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error translating textbook to multiple languages:', error);
      throw error;
    }
  },

  /**
   * Get translation status for a textbook
   */
  getTranslationStatus: async (textbookId: string): Promise<any> => {
    try {
      const response = await apiClient.get(`/translation/status/${textbookId}`);
      return response.data;
    } catch (error) {
      console.error('Error getting translation status:', error);
      throw error;
    }
  },

  /**
   * Get supported translation languages
   */
  getSupportedLanguages: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/translation/supported-languages');
      return response.data;
    } catch (error) {
      console.error('Error getting supported languages:', error);
      throw error;
    }
  },

  /**
   * Validate if translation to the specified language is supported
   */
  validateLanguageSupport: async (languageCode: string): Promise<any> => {
    try {
      const response = await apiClient.get(`/translation/validate-language/${languageCode}`);
      return response.data;
    } catch (error) {
      console.error('Error validating language support:', error);
      throw error;
    }
  },

  /**
   * Check the health of the translation service
   */
  healthCheck: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/translation/health');
      return response.data;
    } catch (error) {
      console.error('Error checking translation health:', error);
      throw error;
    }
  },
};

export default translationApi;