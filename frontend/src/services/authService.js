/**
 * Authentication Service
 * Handles all authentication-related API calls
 */

import api from './api';

export const authService = {
  /**
   * Register a new user
   * @param {string} email - User email
   * @param {string} password - User password
   * @param {string} fullName - User's full name
   * @returns {Promise} API response
   */
  async register(email, password, fullName) {
    try {
      const response = await api.post('/auth/register', {
        email,
        password,
        full_name: fullName,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Registration failed' };
    }
  },

  /**
   * Login user and store token
   * @param {string} email - User email
   * @param {string} password - User password
   * @returns {Promise} API response with token and user data
   */
  async login(email, password) {
    try {
      const response = await api.post('/auth/login', {
        email,
        password,
      });

      if (response.data.success) {
        const { token, user } = response.data.data;

        // Store token and user in localStorage
        localStorage.setItem('fncs_token', token);
        localStorage.setItem('fncs_user', JSON.stringify(user));
      }

      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Login failed' };
    }
  },

  /**
   * Logout user and clear stored data
   * @returns {Promise} API response
   */
  async logout() {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      // Continue with logout even if API call fails
      console.error('Logout API call failed:', error);
    } finally {
      // Always clear local storage
      localStorage.removeItem('fncs_token');
      localStorage.removeItem('fncs_user');
    }
  },

  /**
   * Verify if current token is valid
   * @returns {Promise} API response
   */
  async verifyToken() {
    try {
      const response = await api.get('/auth/verify');
      return response.data;
    } catch (error) {
      throw error.response?.data || { error: 'Token verification failed' };
    }
  },

  /**
   * Get current user from localStorage
   * @returns {Object|null} User object or null
   */
  getCurrentUser() {
    try {
      const userStr = localStorage.getItem('fncs_user');
      return userStr ? JSON.parse(userStr) : null;
    } catch (error) {
      console.error('Error parsing user data:', error);
      return null;
    }
  },

  /**
   * Check if user is authenticated
   * @returns {boolean} True if token exists
   */
  isAuthenticated() {
    return !!localStorage.getItem('fncs_token');
  },

  /**
   * Get current JWT token
   * @returns {string|null} JWT token or null
   */
  getToken() {
    return localStorage.getItem('fncs_token');
  },
};

export default authService;
