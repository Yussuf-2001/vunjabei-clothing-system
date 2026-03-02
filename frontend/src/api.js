import axios from 'axios';

// allow overriding from environment (useful for local development)
// Vite exposes variables prefixed with VITE_ through import.meta.env
let rawBaseUrl = import.meta.env.VITE_API_URL;

// if no environment var supplied, and we are running in a browser, try to use
// the current origin (helpful when dev server and API share localhost).
if (!rawBaseUrl && typeof window !== 'undefined' && window.location) {
  const { hostname, protocol } = window.location;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    // backend usually runs on port 8000 during development
    rawBaseUrl = `${protocol}//${hostname}:8000/api`;
  }
}

// final fallback to production URL if nothing else available
rawBaseUrl = rawBaseUrl || "https://vunjabei-clothing-system.onrender.com/api";

const baseURL = rawBaseUrl.endsWith('/') ? rawBaseUrl : `${rawBaseUrl}/`;

const api = axios.create({
  baseURL,
  withCredentials: true,
});

export default api;
