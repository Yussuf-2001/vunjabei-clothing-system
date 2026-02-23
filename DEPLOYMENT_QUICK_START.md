# Deployment Quick Start

## Backend (Render)
1. Connect GitHub repository.
2. Build: `./build.sh`
3. Start: `gunicorn vunjabei.wsgi`
4. Add env vars (`SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS`, CORS/CSRF values).

## Frontend (Vercel/Netlify)
1. Root directory: `frontend`
2. Build: `npm run build`
3. Output: `dist`
4. Env: `VITE_API_BASE_URL=https://<backend>/api/`

## Required Checks
- `/api/health/` returns status ok.
- Login works for admin and customer.
- Product list loads.
- Order flow works end-to-end.
