// API Configuration
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1' ||
                     window.location.hostname.includes('localhost');

// Force production URLs for deployed app
const PRODUCTION_BASE = 'https://chestnutminnow.onpella.app';
const DEVELOPMENT_BASE = 'http://localhost:5000';

export const API_CONFIG = {
  BASE_URL: isDevelopment ? DEVELOPMENT_BASE : PRODUCTION_BASE,
  API_BASE_URL: isDevelopment ? `${DEVELOPMENT_BASE}/api` : `${PRODUCTION_BASE}/api`,
  TIMEOUT: 30000,
};

// Debug logging
console.log('API Config:', {
  hostname: window.location.hostname,
  isDevelopment,
  BASE_URL: API_CONFIG.BASE_URL,
  API_BASE_URL: API_CONFIG.API_BASE_URL
});

// Helper function to get full API endpoint
export const getApiUrl = (endpoint) => {
  const url = `${API_CONFIG.API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  console.log('API URL:', url);
  return url;
};

// Helper function for non-API endpoints (like contact)
export const getBaseUrl = (endpoint) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
  console.log('Base URL:', url);
  return url;
};