import axios, { AxiosResponse } from 'axios';
import {
  ExportFormat,
  ExportStatus,
  ExportTextbookResponse,
  Textbook
} from '../../types/textbook';

// Base API URL - in a real application, this would be configured via environment variables
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance with default configuration
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000, // 60 second timeout for export operations
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
 * API service for textbook export functionality
 */
export const exportApi = {
  /**
   * Export a textbook in the specified format
   */
  exportTextbook: async (
    textbookId: string,
    formatName: string,
    outputLocation?: string
  ): Promise<ExportTextbookResponse> => {
    try {
      const formData = new FormData();
      formData.append('textbook_id', textbookId);
      formData.append('format_name', formatName);

      if (outputLocation) {
        formData.append('output_path', outputLocation);
      }

      const response: AxiosResponse<ExportTextbookResponse> = await apiClient.post(
        '/export/generate',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error exporting textbook:', error);
      throw error;
    }
  },

  /**
   * Get a list of supported export formats
   */
  getSupportedFormats: async (): Promise<ExportFormat[]> => {
    try {
      const response: AxiosResponse<ExportFormat[]> = await apiClient.get(
        '/export/formats'
      );
      return response.data;
    } catch (error) {
      console.error('Error getting supported formats:', error);
      throw error;
    }
  },

  /**
   * Get the export status for a textbook
   */
  getExportStatus: async (textbookId: string): Promise<ExportStatus> => {
    try {
      const response: AxiosResponse<ExportStatus> = await apiClient.get(
        `/export/status/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting export status:', error);
      throw error;
    }
  },

  /**
   * Validate export parameters before starting the export process
   */
  validateExportParams: async (
    textbookId: string,
    formatName: string
  ): Promise<{ valid: boolean; message: string; details?: any }> => {
    try {
      const formData = new FormData();
      formData.append('textbook_id', textbookId);
      formData.append('format_name', formatName);

      const response = await apiClient.post(
        '/export/validate',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error validating export parameters:', error);
      throw error;
    }
  },

  /**
   * Get details of a specific textbook (from the generation API)
   */
  getTextbook: async (textbookId: string): Promise<Textbook> => {
    try {
      // This uses the generation API endpoint, but we include it here for convenience
      const response: AxiosResponse<Textbook> = await apiClient.get(
        `/textbook-generation/${textbookId}`
      );
      return response.data;
    } catch (error) {
      console.error('Error getting textbook for export:', error);
      throw error;
    }
  },

  /**
   * Download an exported textbook file
   */
  downloadExportedTextbook: async (textbookId: string, formatName: string): Promise<Blob> => {
    try {
      const response = await apiClient.get(
        `/export/download/${textbookId}/${formatName}`,
        {
          responseType: 'blob', // Important: return as blob for file download
        }
      );
      return response.data;
    } catch (error) {
      console.error('Error downloading exported textbook:', error);
      throw error;
    }
  },

  /**
   * Get export history for a textbook
   */
  getExportHistory: async (textbookId: string): Promise<any[]> => {
    // Note: This would require a backend endpoint that may not exist yet
    // For now, we'll return an empty array
    console.warn('Export history endpoint not implemented on backend');
    return [];
  },

  /**
   * Delete an exported file (if supported by backend)
   */
  deleteExportedFile: async (textbookId: string, formatName: string): Promise<{ success: boolean; message: string }> => {
    // Note: This endpoint would need to be implemented on the backend
    // For now, we'll return a mock response
    console.warn('Delete exported file endpoint not implemented on backend');
    return {
      success: false,
      message: 'Delete exported file not yet supported by the backend',
    };
  },
};

export default exportApi;