// API Configuration
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

export const API_CONFIG = {
  BASE_URL: isDevelopment ? 'http://localhost:5000' : 'https://terra-cottapigeon.onpella.app',
  API_BASE_URL: isDevelopment ? 'http://localhost:5000/api' : 'https://terra-cottapigeon.onpella.app/api',
  TIMEOUT: 30000, // 30 seconds - increased timeout
};

// Helper function to get full API endpoint
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};

// Helper function for non-API endpoints (like contact)
export const getBaseUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};