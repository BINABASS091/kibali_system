import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
    }

    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (username, password) => 
    apiClient.post('/login/', { username, password }),
};

export const permitAPI = {
  create: (permitData) => 
    apiClient.post('/permits/create/', permitData),
  list: () => 
    apiClient.get('/permits/'),
  getDetail: (permitId) => 
    apiClient.get(`/permits/${permitId}/`),
  download: (permitId) => 
    apiClient.get(`/permits/${permitId}/download/`, { responseType: 'blob' }),
};
