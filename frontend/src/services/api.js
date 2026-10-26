import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
});

export const api = {
  // Threat Scanners
  scanUrl: async (url) => {
    const response = await client.post('/predict/url', { url });
    return response.data;
  },

  scanNetwork: async (file = null) => {
    if (file) {
      const formData = new FormData();
      formData.append('file', file);
      const response = await client.post('/predict/network', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } else {
      const response = await client.post('/predict/network');
      return response.data;
    }
  },

  scanLogin: async (eventData) => {
    const response = await client.post('/predict/login', eventData);
    return response.data;
  },

  // Alerts & Triage
  getAlerts: async (params = {}) => {
    const response = await client.get('/alerts', { params });
    return response.data;
  },

  reviewAlert: async (alertId, verdict, notes = '') => {
    const response = await client.patch(`/alerts/${alertId}/review`, {
      analyst_verdict: verdict,
      analyst_notes: notes
    });
    return response.data;
  },

  // Dashboard Stats
  getDashboardStats: async () => {
    const response = await client.get('/dashboard/stats');
    return response.data;
  },

  // Models & Datasets Information (Zero hardcoding)
  getModelsInfo: async () => {
    const response = await client.get('/models/info');
    return response.data;
  },

  // Feedback Retraining
  retrainModel: async (module = 'all') => {
    const response = await client.post('/retrain', { module });
    return response.data;
  }
};

export default api;
