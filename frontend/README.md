# Frontend Notes

This folder contains the React client for Vunjabei Clothing Management System.

## Commands
```bash
npm install
npm run dev
npm run build
```

## Local Development Order
1. Start backend first (`../manage.py runserver` or `../start-dev.ps1`).
2. Start frontend (`npm run dev`).

## Environment Variable
The client uses `VITE_API_URL` to know where the Django API lives. When you run the
React dev server locally it will automatically default to
`http://localhost:8000/api/` so you don't have to set anything – the value is only
required if your backend is hosted elsewhere (Render, etc.).

To override manually you can create a `.env` file in the `frontend` folder with:

```bash
VITE_API_URL=http://127.0.0.1:8000/api/   # change to your backend URL if necessary
```

> **Important:** restart the dev server after changing environment variables.

