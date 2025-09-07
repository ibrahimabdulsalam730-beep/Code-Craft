// API Configuration
export const API_CONFIG = {
  BASE_URL: 'https://kelly-greenrhinoceros.onpella.app/api',
  TIMEOUT: 10000, // 10 seconds
};

// Helper function to get full API endpoint
export const getApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;
};