import axios, { AxiosResponse } from 'axios';
import {
  GenerationParams,
  GenerateTextbookResponse,
  Textbook,
  GenerationStatus,
  TextbookPreview,
  ChapterPreview,
  TableOfContents,
  TextbookMetadata
} from '../../types/textbook';

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
 * API service for textbook generation functionality
 */
export const textbookGenerationApi = {
  /**
   * Generate a new textbook based on the provided parameters
   */
  generateTextbook: async (params: GenerationParams): Promise<GenerateTextbookResponse> => {
    try {
      const response: AxiosResponse<GenerateTextbookResponse> = await apiClient.post(
        '/textbook-generation/generate',
        {
          ...params,
          // Ensure numeric values are properly formatted
          numChapters: Number(params.numChapters),
          sectionsPerChapter: Number(params.sectionsPerChapter),
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error generating textbook:', error);
      throw error;
    }
  },

  /**
   * Get the current status of a textbook generation process
   */
  getGenerationStatus: async (textbookId: string): Promise<GenerationStatus> => {
    try {
      const response: AxiosResponse<GenerationStatus> = await apiClient.get(
        `/textbook-generation/status/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting generation status:', error);
      throw error;
    }
  },

  /**
   * Get details of a specific textbook
   */
  getTextbook: async (textbookId: string): Promise<Textbook> => {
    try {
      const response: AxiosResponse<Textbook> = await apiClient.get(
        `/textbook-generation/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting textbook:', error);
      throw error;
    }
  },

  /**
   * List all textbooks in the system
   */
  listTextbooks: async (): Promise<Textbook[]> => {
    try {
      const response: AxiosResponse<Textbook[]> = await apiClient.get(
        '/textbook-generation/list'
      );
      return response.data;
    } catch (error) {
      console.error('Error listing textbooks:', error);
      throw error;
    }
  },

  /**
   * Get a preview of textbook content
   */
  getTextbookPreview: async (textbookId: string): Promise<TextbookPreview> => {
    try {
      const response: AxiosResponse<TextbookPreview> = await apiClient.get(
        `/preview/content/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting textbook preview:', error);
      throw error;
    }
  },

  /**
   * Get a preview of a specific chapter
   */
  getChapterPreview: async (textbookId: string, chapterNumber: number): Promise<ChapterPreview> => {
    try {
      const response: AxiosResponse<ChapterPreview> = await apiClient.get(
        `/preview/chapter/${textbookId}/${chapterNumber}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting chapter preview:', error);
      throw error;
    }
  },

  /**
   * Get the table of contents for a textbook
   */
  getTableOfContents: async (textbookId: string): Promise<TableOfContents> => {
    try {
      const response: AxiosResponse<TableOfContents> = await apiClient.get(
        `/preview/toc/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting table of contents:', error);
      throw error;
    }
  },

  /**
   * Get metadata for a textbook
   */
  getTextbookMetadata: async (textbookId: string): Promise<TextbookMetadata> => {
    try {
      const response: AxiosResponse<TextbookMetadata> = await apiClient.get(
        `/preview/metadata/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting textbook metadata:', error);
      throw error;
    }
  },

  /**
   * Cancel a textbook generation process (if supported by backend)
   */
  cancelGeneration: async (textbookId: string): Promise<{ success: boolean; message: string }> => {
    try {
      // Note: This endpoint would need to be implemented on the backend
      // For now, we'll return a mock response
      console.warn('Cancel generation endpoint not implemented on backend');
      return {
        success: false,
        message: 'Cancel generation not yet supported by the backend',
      };
    } catch (error) {
      console.error('Error canceling generation:', error);
      throw error;
    }
  },
};

export default textbookGenerationApi;