import axios from 'axios';

const rawBaseUrl = "https://vunjabei-clothing-system.onrender.com/api";

const baseURL = rawBaseUrl.endsWith('/') ? rawBaseUrl : `${rawBaseUrl}/`;

const api = axios.create({
  baseURL,
});

export default api;
