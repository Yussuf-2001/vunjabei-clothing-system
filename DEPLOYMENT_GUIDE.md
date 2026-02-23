﻿# Deployment Guide

## Target Architecture
- Backend API: Render Web Service
- Frontend UI: Vercel or Netlify
- Database: PostgreSQL (Render Postgres or managed Postgres)

## 1. Backend Deployment (Render)
1. Push project to GitHub.
2. On Render, create a new Web Service from the repository.
3. Set root directory to `backend` repository root (current folder).
4. Build command:
```bash
./build.sh
```
5. Start command:
```bash
gunicorn vunjabei.wsgi
```
6. Add environment variables:
- `SECRET_KEY`
- `DEBUG=False`
- `ALLOWED_HOSTS=<your-render-domain>`
- `DATABASE_URL=<postgres-connection-url>`
- `CORS_ALLOWED_ORIGINS=<frontend-domain>`
- `CSRF_TRUSTED_ORIGINS=<frontend-domain>`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `CLOUDINARY_CLOUD_NAME=<your-cloud-name>`
- `CLOUDINARY_API_KEY=<your-api-key>`
- `CLOUDINARY_API_SECRET=<your-api-secret>`

## 2. Frontend Deployment (Vercel/Netlify)
1. Import the same repository and set project root to `frontend`.
2. Build command:
```bash
npm run build
```
3. Output directory:
```bash
dist
```
4. Add environment variable:
- `VITE_API_BASE_URL=https://<your-backend-domain>/api/`

## 3. Post-Deployment Validation
- Open frontend URL.
- Test registration and login.
- Test product list loading.
- Place an order as customer.
- Update order status as admin.
- Check backend health endpoint `/api/health/`.

## 4. Evidence to Capture
- Screenshot of public frontend URL
- Screenshot of backend API health URL
- Screenshot of GitHub commit history
- Screenshot of key features running (admin + customer)
