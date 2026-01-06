/**
 * Authentication Context
 * Provides authentication state and functions to all components
 * Manages user login/logout state
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { getToken, removeToken, setToken, getCurrentUser } from '../services/api';

// Create the context
const AuthContext = createContext();

/**
 * Custom hook to use authentication context
 * Use this in components to access auth state and functions
 */
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

/**
 * AuthProvider component
 * Wraps the app and provides authentication state
 */
export const AuthProvider = ({ children }) => {
  // State to track if user is authenticated
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  /**
   * Check if user is logged in on app load
   * Verifies if token exists and is valid
   */
  useEffect(() => {
    const checkAuth = async () => {
      const token = getToken();
      if (token) {
        try {
          // Try to get current user to verify token is valid
          const userData = await getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          // Token is invalid, remove it
          removeToken();
          setIsAuthenticated(false);
          setUser(null);
        }
      }
      setLoading(false);
    };

    checkAuth();
  }, []);

  /**
   * Login function
   * Saves token and updates auth state
   */
  const login = (token, userData) => {
    setToken(token);
    setUser(userData);
    setIsAuthenticated(true);
  };

  /**
   * Logout function
   * Removes token and clears auth state
   */
  const logout = () => {
    removeToken();
    setUser(null);
    setIsAuthenticated(false);
  };

  // Value to provide to context consumers
  const value = {
    isAuthenticated,
    user,
    loading,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};










