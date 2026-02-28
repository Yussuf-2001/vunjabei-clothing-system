from django.db import migrations
import os


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

    if not User.objects.filter(username=username).exists():
        print(f"Creating superuser: {username}")
        User.objects.create_superuser(username=username, email=email, password=password)
    else:
        print(f"Superuser '{username}' already exists.")


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_order_address_order_phone_order_status'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
