import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Auth API
export const authAPI = {
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
  
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  
  logout: (sessionToken) =>
    api.post('/auth/logout', { session_token: sessionToken }),
  
  adminLogin: (username, password) =>
    api.post('/auth/admin/login', { username, password }),
};

// Feedback API
export const feedbackAPI = {
  submit: (sessionToken, rating, comment) =>
    api.post('/feedback', { session_token: sessionToken, rating, comment }),
  
  getAll: (sessionToken, filters = {}) => {
    const params = { session_token: sessionToken, ...filters };
    return api.get('/feedback', { params });
  },
};

// Admin API
export const adminAPI = {
  getStats: (sessionToken) =>
    api.get('/admin/stats', { params: { session_token: sessionToken } }),
};

export default api;
