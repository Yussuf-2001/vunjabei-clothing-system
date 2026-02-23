import axios from 'axios';

const fallbackBaseUrl = `${window.location.protocol}//${window.location.hostname}:8000/api/`;

const rawBaseUrl =
  import.meta.env.VITE_API_BASE_URL || fallbackBaseUrl;

const baseURL = rawBaseUrl.endsWith('/') ? rawBaseUrl : `${rawBaseUrl}/`;

const api = axios.create({
  baseURL,
  withCredentials: true,
});

export default api;
