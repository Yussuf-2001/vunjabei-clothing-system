#!/usr/bin/env python
"""Test script to check image storage and Cloudinary configuration"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vunjabei.settings')
django.setup()

from django.conf import settings
from myapp.models import Product

print("=" * 60)
print("IMAGE STORAGE CONFIGURATION")
print("=" * 60)

print(f"\n1. CLOUDINARY CONFIGURED: {settings.USE_CLOUDINARY}")
print(f"2. DEFAULT FILE STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"3. MEDIA_URL: {settings.MEDIA_URL}")
print(f"4. MEDIA_ROOT: {settings.MEDIA_ROOT}")

print(f"\nCloudinary Environment Variables:")
print(f"  - CLOUD_NAME: {os.environ.get('CLOUDINARY_CLOUD_NAME', 'NOT SET')}")
print(f"  - API_KEY: {'SET' if os.environ.get('CLOUDINARY_API_KEY') else 'NOT SET'}")
print(f"  - API_SECRET: {'SET' if os.environ.get('CLOUDINARY_API_SECRET') else 'NOT SET'}")

print(f"\n5. STORAGES CONFIG:")
print(f"  - default backend: {settings.STORAGES['default']['BACKEND']}")
print(f"  - staticfiles backend: {settings.STORAGES['staticfiles']['BACKEND']}")

print(f"\n6. Products with images:")
products = Product.objects.filter(image__isnull=False, image__exact='')[:5]
print(f"   Total products with images: {Product.objects.filter(image__isnull=False).exclude(image__exact='').count()}")

for product in Product.objects.filter(image__isnull=False).exclude(image__exact='')[:3]:
    print(f"\n   Product: {product.name}")
    print(f"   - Image field: {product.image}")
    print(f"   - Image URL: {product.image.url if hasattr(product.image, 'url') else 'NO URL ATTR'}")
    print(f"   - Image name: {product.image.name if hasattr(product.image, 'name') else 'NO NAME'}")

print("\n" + "=" * 60)
