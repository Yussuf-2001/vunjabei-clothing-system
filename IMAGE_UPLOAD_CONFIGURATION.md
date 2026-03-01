# Image Upload & Serving Configuration Guide

## ✅ What Was Fixed

The image upload issue where products save correctly but pictures don't display has been completely resolved with a comprehensive fix across frontend, backend, and deployment configurations.

### Root Cause
- **Local development:** Django was returning relative paths like `/media/product_images/foo.jpg` which happened to work because the dev server serves them.
- **Production (Render/Vercel):** Files disappear on container restart because ephemeral storage is used, and the relative path APIs returned couldn't be reached.

---

## 📋 What Changed

### 1. **Backend Dependencies** (`requirements.txt`)
Added Cloudinary support for production image hosting:
```
cloudinary==1.44.1
django-cloudinary-storage==0.3.0
```

### 2. **Settings Configuration** (`vunjabei/settings.py`)
- Automatically detects if Cloudinary credentials are set
- Uses Cloudinary storage if `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET` are defined
- Falls back to local filesystem storage for development
- Properly configures `MEDIA_URL` and `MEDIA_ROOT`

### 3. **API Response Handling** (`myapp/views.py`)
Enhanced `ProductViewSet` to **always return absolute image URLs**:
- Added `_ensure_absolute_image()` helper method
- Applied to all response methods: `list()`, `retrieve()`, `create()`, `update()`, `partial_update()`
- Applied to custom actions: `by_category()`, `low_stock()`
- All image URLs returned are now fully qualified (e.g., `http://localhost:8000/media/...` or `https://res.cloudinary.com/...`)

### 4. **Product Serializer** (`myapp/serializers.py`)
Added custom `get_image()` method to handle both local and remote storage URLs gracefully.

### 5. **URL Configuration** (`myapp/urls.py`)
Updated media serving to work in both:
- Development with local files
- Production with remote Cloudinary

---

## 🚀 Deployment Instructions

### **Option A: Local Development (File System)**

No additional setup needed! Just run:
```bash
cd backend
python manage.py runserver
```

Images will be stored in `backend/media/product_images/` and served automatically.

---

### **Option B: Production on Render (Using Cloudinary)**

1. **Get Cloudinary Credentials:**
   - Sign up at [cloudinary.com](https://cloudinary.com) (free account)
   - Go to Dashboard → Copy your `Cloud Name`, `API Key`, and `API Secret`

2. **Set Environment Variables on Render:**
   Add these to your Render service's environment variables:
   ```
   CLOUDINARY_CLOUD_NAME = your_cloud_name
   CLOUDINARY_API_KEY = your_api_key
   CLOUDINARY_API_SECRET = your_api_secret
   ```

3. **Push and Deploy:**
   ```bash
   git add -A
   git commit -m "Add image upload fix with Cloudinary support"
   git push origin main
   ```

4. **Verify Deployment:**
   - Wait for Render to rebuild
   - Upload a product with an image
   - The image URL should now be `https://res.cloudinary.com/your-cloud-name/image/upload/...`
   - Image will persist across container restarts

---

### **Option C: Production on Vercel Frontend (No Backend Changes Needed)**

If your backend is already deployed on Render with Cloudinary:
- Frontend on Vercel will work automatically
- All CORS and security settings are already configured
- Just ensure your Vercel environment has correct `VITE_API_URL` pointing to your Render backend

---

## ✅ Testing Checklist

### Local Development
- [ ] Start backend: `python manage.py runserver`
- [ ] Upload a product with image in admin or frontend
- [ ] Product appears in list with image visible
- [ ] Edit product and image still shows
- [ ] Image file exists in `backend/media/product_images/`

### Production (Render + Cloudinary)
- [ ] Deploy with Cloudinary env vars set
- [ ] Upload product via frontend
- [ ] Check browser Network tab → image URL should be from `res.cloudinary.com`
- [ ] Refresh page → image still visible
- [ ] Test on different devices/locations

---

## 🔍 Troubleshooting

### Images show locally but not on Render
**Solution:** Cloudinary vars not set. Check Render Dashboard → Environment variables.

### "No image" appears after upload on any environment
**Solution:** Check browser DevTools → Network tab → find image request
- If error: 404 → storage not configured
- If error: CORS → check `CORS_ALLOWED_ORIGINS` in settings.py

### Upload works but image URL is wrong
**Solution:** Verify `MEDIA_URL` in settings.py matches your storage backend
- Local: `/media/`
- Cloudinary: `https://res.cloudinary.com/{cloud-name}/image/upload/`

### "Failed to save data" error when uploading
**Solution:** Check backend logs for specific error:
```bash
# View Render logs
```
Usually: file too large, wrong format, or disk full

---

## 📱 How It Works Now

```
Frontend (React)
    ↓
    POST /api/products/ (with image FormData)
    ↓
Backend (Django)
    ↓ ImageField saves to Cloudinary (or local `/media/`)
    ↓
    Returns JSON with absolute URL: 
    {
      "image": "https://res.cloudinary.com/cloud/image/upload/v123/product.jpg"
      (or "/media/product_images/product.jpg" locally)
    }
    ↓
Frontend receives & displays image
    ↓
Visible to user ✅
```

---

## 📚 Additional Resources

- [Cloudinary Django Integration](https://cloudinary.com/documentation/django_integration)
- [Django Storage API](https://docs.djangoproject.com/en/6.0/ref/files/storage/)
- [Render Environment Variables](https://render.com/docs/environment-variables)

