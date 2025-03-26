import axios from 'axios'

// Determine API base URL based on environment
const getBaseUrl = () => {
  // For local development outside Docker, use the full URL
  if (process.env.NODE_ENV === 'development' && window.location.hostname === 'localhost' && window.location.port === '8080') {
    return 'http://localhost:8000/api';
  }
  
  // Inside Docker or production, use relative URL (handled by Nginx proxy)
  return '/api';
};

// API client configuration
const apiClient = axios.create({
  baseURL: getBaseUrl(),
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 10 second timeout
});

// Error handling interceptor
apiClient.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.message || 'Unknown error');
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
    }
    return Promise.reject(error);
  }
);

export default {
  // Get all cameras
  getCameras() {
    return apiClient.get('/cameras/')
  },
  
  // Get a specific camera
  getCamera(id) {
    return apiClient.get(`/cameras/${id}/`)
  },
  
  // Create a new camera
  createCamera(data) {
    return apiClient.post('/cameras/', data)
  },
  
  // Update a camera
  updateCamera(id, data) {
    return apiClient.put(`/cameras/${id}/`, data)
  },
  
  // Delete a camera
  deleteCamera(id) {
    return apiClient.delete(`/cameras/${id}/`)
  },
  
  // Start streaming for a camera
  startStream(id) {
    return apiClient.post(`/cameras/${id}/start/`)
  },
  
  // Stop streaming for a camera
  stopStream(id) {
    return apiClient.post(`/cameras/${id}/stop/`)
  },
  
  // Restart streaming for a camera
  restartStream(id) {
    return apiClient.post(`/cameras/${id}/restart/`)
  }
} 