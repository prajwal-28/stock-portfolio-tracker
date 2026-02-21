/**
 * API Service
 * Handles all HTTP requests to the FastAPI backend
 * Manages JWT token storage and automatic token attachment to requests
 */

import axios from 'axios';

// Base URL for the backend API
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://stock-portfolio-tracker-3ntt.onrender.com';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Get JWT token from localStorage
 */
export const getToken = () => {
  return localStorage.getItem('token');
};

/**
 * Save JWT token to localStorage
 */
export const setToken = (token) => {
  localStorage.setItem('token', token);
};

/**
 * Remove JWT token from localStorage (logout)
 */
export const removeToken = () => {
  localStorage.removeItem('token');
};

/**
 * Interceptor to automatically attach JWT token to requests
 * This runs before every API request
 */
api.interceptors.request.use(
  (config) => {
    const token = getToken();
    if (token) {
      // Attach token to Authorization header
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Interceptor to handle API responses and errors
 * This runs after every API response
 */
api.interceptors.response.use(
  (response) => {
    // If response is successful, just return it
    return response;
  },
  (error) => {
    // If we get a 401 (Unauthorized), the token is invalid
    // Remove token and redirect to login
    if (error.response && error.response.status === 401) {
      removeToken();
      // Redirect to login page
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ============ AUTHENTICATION API ============

/**
 * Register a new user
 * @param {Object} userData - { username, email, password }
 * @returns {Promise} API response with token and user data
 */
export const register = async (userData) => {
  const response = await api.post('/api/auth/register', userData);
  return response.data;
};

/**
 * Login user
 * @param {Object} credentials - { username, password }
 * @returns {Promise} API response with token and user data
 */
export const login = async (credentials) => {
  const response = await api.post('/api/auth/login', credentials);
  return response.data;
};

/**
 * Get current user information
 * @returns {Promise} API response with user data
 */
export const getCurrentUser = async () => {
  const response = await api.get('/api/auth/me');
  return response.data;
};

// ============ PORTFOLIO API ============

/**
 * Get all stocks in portfolio
 * @returns {Promise} API response with array of stocks
 */
export const getStocks = async () => {
  const response = await api.get('/api/portfolio/stocks');
  return response.data;
};

/**
 * Get a single stock by ID
 * @param {string} stockId - Stock ID
 * @returns {Promise} API response with stock data
 */
export const getStock = async (stockId) => {
  const response = await api.get(`/api/portfolio/stocks/${stockId}`);
  return response.data;
};

/**
 * Add a new stock to portfolio
 * @param {Object} stockData - { stock_name, quantity, buy_price }
 * @returns {Promise} API response with created stock data
 */
export const addStock = async (stockData) => {
  const response = await api.post('/api/portfolio/stocks', stockData);
  return response.data;
};

/**
 * Update an existing stock
 * @param {string} stockId - Stock ID
 * @param {Object} stockData - Partial stock data to update
 * @returns {Promise} API response with updated stock data
 */
export const updateStock = async (stockId, stockData) => {
  const response = await api.put(`/api/portfolio/stocks/${stockId}`, stockData);
  return response.data;
};

/**
 * Delete a stock from portfolio
 * @param {string} stockId - Stock ID
 * @returns {Promise} API response
 */
export const deleteStock = async (stockId) => {
  const response = await api.delete(`/api/portfolio/stocks/${stockId}`);
  return response.data;
};

/**
 * Get portfolio summary with totals
 * @returns {Promise} API response with summary data
 */
export const getPortfolioSummary = async () => {
  const response = await api.get('/api/portfolio/summary');
  return response.data;
};

export default api;










