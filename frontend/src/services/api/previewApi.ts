import axios, { AxiosResponse } from 'axios';
import {
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
  timeout: 15000, // 15 second timeout
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
 * API service for textbook preview functionality
 */
export const previewApi = {
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
   * Get a preview of multiple chapters
   */
  getMultipleChapterPreviews: async (
    textbookId: string,
    chapterNumbers: number[]
  ): Promise<ChapterPreview[]> => {
    try {
      // In a real implementation, this might be a single endpoint that accepts multiple chapter numbers
      // For now, we'll make multiple requests
      const promises = chapterNumbers.map(num =>
        apiClient.get<ChapterPreview>(`/preview/chapter/${textbookId}/${num}`)
      );

      const responses = await Promise.all(promises);
      return responses.map(response => response.data);
    } catch (error) {
      console.error('Error getting multiple chapter previews:', error);
      throw error;
    }
  },

  /**
   * Get a full content preview (if the content is not too large)
   */
  getFullContentPreview: async (textbookId: string): Promise<TextbookPreview> => {
    try {
      // This would potentially get the full content preview, but we need to be careful about response size
      const response: AxiosResponse<TextbookPreview> = await apiClient.get(
        `/preview/content/${textbookId}`
      );

      // If the preview is already the full content, return it
      // Otherwise, we might need a different endpoint for full content
      if (response.data.fullContentAvailable) {
        return response.data;
      } else {
        // For large content, we might need to fetch sections separately
        console.warn('Full content not available in preview. Consider implementing chunked content retrieval.');
        return response.data;
      }
    } catch (error) {
      console.error('Error getting full content preview:', error);
      throw error;
    }
  },

  /**
   * Search within textbook content
   */
  searchInTextbook: async (
    textbookId: string,
    query: string,
    maxResults: number = 10
  ): Promise<{ results: Array<{ chapter: string; section: string; content: string; relevance: number }> }> => {
    // Note: This endpoint would need to be implemented on the backend
    // For now, we'll return a mock response
    console.warn('Search in textbook endpoint not implemented on backend');
    return {
      results: [],
    };
  },

  /**
   * Get content statistics for a textbook
   */
  getContentStats: async (textbookId: string): Promise<{
    totalWords: number;
    avgWordsPerChapter: number;
    avgWordsPerSection: number;
    contentComplexity: string;
  }> => {
    try {
      // Get metadata which includes word count
      const metadata = await apiClient.get<TextbookMetadata>(`/preview/metadata/${textbookId}`);

      const avgWordsPerChapter = metadata.data.totalChapters > 0
        ? Math.round(metadata.data.wordCount / metadata.data.totalChapters)
        : 0;

      // This is a simplified calculation - in a real implementation,
      // the backend would calculate this more accurately
      const avgWordsPerSection = avgWordsPerChapter > 0
        ? Math.round(avgWordsPerChapter / 3) // Assuming ~3 sections per chapter
        : 0;

      // Determine complexity based on average sentence length and vocabulary
      let contentComplexity = 'medium';
      if (metadata.data.contentDepth === 'shallow') {
        contentComplexity = 'low';
      } else if (metadata.data.contentDepth === 'deep') {
        contentComplexity = 'high';
      }

      return {
        totalWords: metadata.data.wordCount,
        avgWordsPerChapter,
        avgWordsPerSection,
        contentComplexity
      };
    } catch (error) {
      console.error('Error getting content stats:', error);
      throw error;
    }
  },
};

export default previewApi;