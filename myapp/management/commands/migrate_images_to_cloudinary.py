from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from django.core.files.storage import default_storage
from pathlib import Path
import os

from myapp.models import Product


class Command(BaseCommand):
    help = (
        "Upload local media product images to the configured storage (e.g. Cloudinary) "
        "and update Product.image fields to point to the uploaded files."
    )

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show files that would be uploaded')
        parser.add_argument('--limit', type=int, default=0, help='Limit number of uploads (0 = all)')

    def handle(self, *args, **options):
        dry = options.get('dry_run', False)
        limit = int(options.get('limit') or 0)

        # Ensure storage is configured (we expect cloudinary when deployed to Render)
        use_cloudinary = getattr(settings, 'USE_CLOUDINARY', False)
        if not use_cloudinary:
            self.stderr.write(self.style.WARNING('Warning: Cloudinary/storage not configured (USE_CLOUDINARY is False).'))
            self.stderr.write('If you are running this on Render, ensure environment variables are set and retry.')
            # still allow dry-run to list files
            if not dry:
                return

        qs = Product.objects.filter(image__isnull=False).exclude(image__exact='')
        total = qs.count()
        self.stdout.write(f'Found {total} products with image entries')

        processed = 0
        for product in qs.order_by('id'):
            if limit and processed >= limit:
                break

            image_field = getattr(product, 'image', None)
            image_name = getattr(image_field, 'name', None)

            if not image_name:
                continue

            # Skip if already an absolute URL (likely already hosted externally)
            if image_name.startswith('http'):
                self.stdout.write(f'Skipping product {product.id}: image field already absolute URL')
                processed += 1
                continue

            # Some deployments store full URL in image.url; detect cloudinary by domain
            try:
                current_url = image_field.url
            except Exception:
                current_url = None

            if current_url and current_url.startswith('http') and 'cloudinary' in current_url:
                self.stdout.write(f'Skipping product {product.id}: already on Cloudinary ({current_url})')
                processed += 1
                continue

            local_root = getattr(settings, 'MEDIA_ROOT', None)
            if not local_root:
                self.stderr.write(f'Unable to determine MEDIA_ROOT; skipping product {product.id}')
                continue

            local_path = Path(local_root) / image_name
            if not local_path.exists():
                self.stderr.write(f'Local file not found for product {product.id}: {local_path}')
                processed += 1
                continue

            if dry:
                self.stdout.write(f'[DRY] Would upload: {local_path} -> {image_name} for product {product.id}')
                processed += 1
                continue

            # Upload using the configured default storage (CloudinaryStorage when configured)
            try:
                with open(local_path, 'rb') as fh:
                    django_file = File(fh)
                    saved_name = default_storage.save(image_name, django_file)

                # Update ImageField to reference the saved name
                product.image.name = saved_name
                product.save(update_fields=['image'])
                self.stdout.write(self.style.SUCCESS(f'Uploaded and updated product {product.id}: {saved_name}'))
            except Exception as exc:
                self.stderr.write(self.style.ERROR(f'Failed to upload product {product.id}: {exc}'))

            processed += 1

        self.stdout.write(self.style.SUCCESS(f'Done. Processed {processed} items (limit={limit}).'))
