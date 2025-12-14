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
 * Interface for authentication credentials
 */
interface AuthCredentials {
  email: string;
  password: string;
  name?: string;
}

/**
 * Interface for user profile
 */
interface UserProfile {
  id: string;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
  preferences: Record<string, any>;
}

/**
 * API service for authentication functionality
 */
export const authApi = {
  /**
   * Register a new user
   */
  register: async (email: string, password: string, name: string = ''): Promise<any> => {
    try {
      const response = await apiClient.post(
        '/auth/register',
        { email, password, name },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  },

  /**
   * Login a user
   */
  login: async (email: string, password: string): Promise<any> => {
    try {
      const response = await apiClient.post(
        '/auth/login',
        { email, password },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  },

  /**
   * Logout the current user
   */
  logout: async (): Promise<any> => {
    try {
      const response = await apiClient.post('/auth/logout');
      // Clear the auth token from local storage
      localStorage.removeItem('authToken');
      return response.data;
    } catch (error) {
      console.error('Logout error:', error);
      // Still remove the token even if the API call fails
      localStorage.removeItem('authToken');
      throw error;
    }
  },

  /**
   * Get the current user's profile
   */
  getProfile: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/auth/profile');
      return response.data;
    } catch (error) {
      console.error('Get profile error:', error);
      throw error;
    }
  },

  /**
   * Update the current user's profile
   */
  updateProfile: async (profileUpdate: Partial<UserProfile>): Promise<any> => {
    try {
      const response = await apiClient.put('/auth/profile', profileUpdate);
      return response.data;
    } catch (error) {
      console.error('Update profile error:', error);
      throw error;
    }
  },

  /**
   * Get personalized textbook recommendations for the user
   */
  getRecommendations: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/auth/recommendations');
      return response.data;
    } catch (error) {
      console.error('Get recommendations error:', error);
      throw error;
    }
  },

  /**
   * Adapt content for the current user based on their preferences
   */
  adaptContent: async (content: string, adaptationType: string = 'difficulty'): Promise<any> => {
    try {
      const response = await apiClient.post('/auth/adapt-content', {
        content,
        adaptation_type: adaptationType
      });
      return response.data;
    } catch (error) {
      console.error('Adapt content error:', error);
      throw error;
    }
  },

  /**
   * Check the health of the auth service
   */
  healthCheck: async (): Promise<any> => {
    try {
      const response = await apiClient.get('/auth/health');
      return response.data;
    } catch (error) {
      console.error('Auth health check error:', error);
      throw error;
    }
  },
};

export default authApi;