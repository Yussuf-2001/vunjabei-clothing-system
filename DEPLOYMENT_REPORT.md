# Deployment Report (One-Page)

## Project
Vunjabei Clothing Management System

## Deployment Objective
Deploy a Django + React application using GitHub-integrated cloud platforms and validate core assignment features on a public URL.

## Deployment Method
- Source control: GitHub repository
- Backend hosting: Render web service
- Frontend hosting: Vercel/Netlify static hosting
- Database: PostgreSQL (managed cloud database)

## Backend Configuration Summary
The backend uses `build.sh` for dependency installation, static collection, and migrations. Runtime uses `gunicorn vunjabei.wsgi` through the `Procfile`. Environment variables are used for `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, and CORS/CSRF settings. The backend was configured to use PostgreSQL only and avoid embedded databases.

## Frontend Configuration Summary
The React frontend reads API URL from `VITE_API_BASE_URL` so that deployment does not depend on localhost. Build is generated via Vite and deployed as static files.

## Validation Performed
- Health endpoint check: `/api/health/`
- Authentication test: register and login
- Product listing test
- Customer order placement test
- Admin order status update test

## Challenges and Fixes
- Legacy template files and duplicate frontend artifacts in backend were removed to keep repository clean.
- Hardcoded local API URL was replaced with environment-based configuration.
- Hardcoded local DB credentials were replaced with environment variables.

## Outcome
The system is deployment-ready with clean backend structure, API-driven architecture, PostgreSQL compliance, and assignment-aligned documentation.
