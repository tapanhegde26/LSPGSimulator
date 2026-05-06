/**
 * API Configuration
 * Loads settings from environment variables with fallbacks
 */

// API URLs from environment or defaults
export const API_CONFIG = {
  baseUrl: import.meta.env.VITE_API_URL || "http://localhost:8000",
  wsUrl: import.meta.env.VITE_WS_URL || "ws://localhost:8000",
} as const;

// API Endpoints
export const ENDPOINTS = {
  health: "/health",
  simulate: "/simulate",
  wsSimulate: "/ws/simulate",
  optimize: "/optimize",
  export: "/export",
} as const;

// Build full URLs
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.baseUrl}${endpoint}`;
};

export const getWsUrl = (endpoint: string): string => {
  return `${API_CONFIG.wsUrl}${endpoint}`;
};
