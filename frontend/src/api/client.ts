import axios from 'axios';

// Vite verwendet VITE_ als Präfix für Umgebungsvariablen
const API_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response Interceptor für allgemeine Fehlerbehandlung
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    return Promise.reject(error);
  }
); 