﻿# Vunjabei Clothing Management System

Full-stack clothing management application built with Django REST API and React frontend.

## 1. Project Description
This system helps a clothing business manage products, customers, and orders using a modern API-driven architecture.

## 2. Technologies Used
- Backend: Django 6 + Django REST Framework
- Frontend: React + Vite + Bootstrap
- Database: PostgreSQL
- Deployment targets: Render (backend), Vercel/Netlify (frontend)

## 3. Assignment Compliance
- Uses Django + React + REST API (no shortcut architecture).
- Uses PostgreSQL and does not depend on embedded SQLite for app configuration.
- Has clear project structure and multiple functional features.
- Includes required project documentation files.

## 4. Core Features
- User authentication (customer self-registration/login, admin/staff created by system admin)
- Product management (CRUD + stock quantity)
- Customer ordering flow and order history
- Admin order management and order status updates
- Dashboard statistics

## 5. Repository Structure
- `manage.py` - Django command runner
- `vunjabei/` - settings, URL configuration, WSGI/ASGI
- `myapp/` - models, serializers, API views, API routes
- `frontend/` - React client
- `requirements.txt` - Python dependencies
- `build.sh`, `Procfile` - deployment helpers
- `INDEX.md` - documentation index

## 6. Environment Setup
### Backend (`.env` from `.env.example`)
- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL` (for deployed environment)
- `CLOUDINARY_CLOUD_NAME` (for media storage)
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- Local PostgreSQL fallback values are already configured in `settings.py`

### Frontend (`frontend/.env` from `frontend/.env.example`)
- `VITE_API_BASE_URL`

## 7. Run Locally
1. Install backend dependencies:
```bash
pip install -r requirements.txt
```
2. Run migrations:
```bash
python manage.py migrate
```
3. Start backend:
```bash
python manage.py runserver
```
4. Start frontend:
```bash
cd frontend
npm install
npm run dev
```

### Quick Start (Windows)
Use one command to start backend and frontend in separate terminals:
```powershell
.\start-dev.ps1
```

## 8. Main API Endpoints
- `GET /api/health/`
- `POST /api/login/`
- `POST /api/register/`
- `POST /api/register-staff/`
- `GET /api/products/`
- `POST /api/place-order/`
- `GET /api/my-orders/`
- `GET /api/orders/` (admin)
- `POST /api/orders/{id}/update-status/` (admin)

## 9. GitHub and Deployment Links
- GitHub Repository: https://github.com/Yussuf-2001/vunjabei-clothing-system
- Backend Live URL: add after deployment
- Frontend Live URL: add after deployment

## 10. Additional Documentation
- `SRS_Document.md`
- `DEPLOYMENT_GUIDE.md`
- `DEPLOYMENT_QUICK_START.md`
- `DEPLOYMENT_REPORT.md`
- `ASSIGNMENT_CHECKLIST.md`
- `PROJECT_SUMMARY.md`
