// API Configuration
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

export const API_CONFIG = {
  BASE_URL: isDevelopment ? 'http://localhost:5000' : 'https://chestnutminnow.onpella.app',
  API_BASE_URL: isDevelopment ? 'http://localhost:5000/api' : 'https://chestnutminnow.onpella.app/api',
  TIMEOUT: 30000,
};

// Helper function to get full API endpoint
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};

// Helper function for non-API endpoints (like contact)
export const getBaseUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};