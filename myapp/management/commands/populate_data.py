from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Category, Product, Customer, Sale, SaleItem
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creating sample data...'))
        
        # Create categories
        categories = [
            # Weka majina ya categories zako mpya hapa ukipenda, au acha wazi
            'Jackets',
            'Pants',
            'Accessories',
            'T-Shirts',
        ]
        
        category_objects = []
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(name=cat_name)
            category_objects.append(cat)
            if created:
                self.stdout.write(f'  ✓ Created category: {cat_name}')
        
        # Create products
        products_data = [
            # Weka bidhaa zako mpya hapa kama unataka kuzi-hardcode
            ('jucket', category_objects[0], Decimal('6000'), 47),
            ('blue jeans', category_objects[1], Decimal('13000'), 37),
            ('backpack', category_objects[2], Decimal('14000'), 47),
            ('T-shirt', category_objects[3], Decimal('5000'), 20),
            ('trouser', category_objects[1], Decimal('3000'), 12),
            ('Cap', category_objects[2], Decimal('4000'), 50),
            ('Cargo Pants', category_objects[1], Decimal('15000'), 25),
        ]
        
        for prod_name, category, price, qty in products_data:
            prod, created = Product.objects.get_or_create(
                name=prod_name,
                defaults={'category': category, 'price': price, 'quantity': qty}
            )
            if created:
                self.stdout.write(f'  ✓ Created product: {prod_name}')
        
        
        customers_data = [
            ('ahmad mh\'d', '0734567890', 'zanzibar'),
            ('Ahmed masoud', '0713396725', 'dar-es-salaam'),
            ('fatma', '0713452367', 'kianga'),
            ('Juma Jux', '0755123456', 'Mbezi'),
            ('Vanessa Mdee', '0766987654', 'morogoro'),
        ]
        
        customer_objects = []
        for cust_name, phone, address in customers_data:
            cust, created = Customer.objects.get_or_create(
                name=cust_name,
                defaults={'phone': phone, 'address': address}
            )
            customer_objects.append(cust)
            if created:
                self.stdout.write(f'  ✓ Created customer: {cust_name}')
        
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('  ✓ Created admin user (username: admin, password: admin123)')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
        
        
        
