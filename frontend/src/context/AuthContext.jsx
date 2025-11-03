/**
 * Authentication Context
 * Provides authentication state and methods to the entire app
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Initialize auth state on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        const currentUser = authService.getCurrentUser();
        if (currentUser && authService.isAuthenticated()) {
          // Verify token is still valid
          try {
            await authService.verifyToken();
            setUser(currentUser);
          } catch (error) {
            // Token invalid, clear auth
            authService.logout();
            setUser(null);
          }
        }
      } catch (error) {
        console.error('Auth initialization error:', error);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  /**
   * Register a new user
   */
  const register = async (email, password, fullName) => {
    setLoading(true);
    setError(null);

    try {
      const result = await authService.register(email, password, fullName);
      setLoading(false);
      return result;
    } catch (error) {
      setError(error.error || 'Registration failed');
      setLoading(false);
      throw error;
    }
  };

  /**
   * Login user
   */
  const login = async (email, password) => {
    setLoading(true);
    setError(null);

    try {
      const result = await authService.login(email, password);
      if (result.success) {
        setUser(result.data.user);
      }
      setLoading(false);
      return result;
    } catch (error) {
      setError(error.error || 'Login failed');
      setLoading(false);
      throw error;
    }
  };

  /**
   * Logout user
   */
  const logout = async () => {
    setLoading(true);
    try {
      await authService.logout();
      setUser(null);
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Clear error
   */
  const clearError = () => {
    setError(null);
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    clearError,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Custom hook to use auth context
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
