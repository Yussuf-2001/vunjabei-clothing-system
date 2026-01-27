from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from clothing.models import Category, Product, Customer, Sale, SaleItem
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Creating sample data...'))
        
        # Create categories
        categories = [
            'T-Shirts',
            'Pants',
            'Jackets',
            'Shoes',
            'Accessories'
        ]
        
        category_objects = []
        for cat_name in categories:
            cat, created = Category.objects.get_or_create(name=cat_name)
            category_objects.append(cat)
            if created:
                self.stdout.write(f'  ✓ Created category: {cat_name}')
        
        # Create products
        products_data = [
            ('Classic T-Shirt', category_objects[0], Decimal('15.99'), 50),
            ('Blue Jeans', category_objects[1], Decimal('49.99'), 30),
            ('Winter Jacket', category_objects[2], Decimal('99.99'), 15),
            ('Running Shoes', category_objects[3], Decimal('79.99'), 25),
            ('Cotton Socks', category_objects[4], Decimal('5.99'), 100),
            ('V-Neck T-Shirt', category_objects[0], Decimal('17.99'), 40),
            ('Khaki Pants', category_objects[1], Decimal('54.99'), 20),
            ('Leather Jacket', category_objects[2], Decimal('199.99'), 10),
        ]
        
        for prod_name, category, price, qty in products_data:
            prod, created = Product.objects.get_or_create(
                name=prod_name,
                defaults={'category': category, 'price': price, 'quantity': qty}
            )
            if created:
                self.stdout.write(f'  ✓ Created product: {prod_name}')
        
        # Create customers
        customers_data = [
            ('John Doe', '0712345678', '123 Main St'),
            ('Jane Smith', '0723456789', '456 Oak Ave'),
            ('James Wilson', '0734567890', '789 Pine Rd'),
            ('Sarah Johnson', '0745678901', '321 Elm St'),
            ('Michael Brown', '0756789012', '654 Maple Dr'),
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
        
        # Create sample sales
        products = list(Product.objects.all())
        sales_count = Sale.objects.count()
        
        if sales_count == 0:
            for i, customer in enumerate(customer_objects[:3]):
                sale = Sale.objects.create(
                    user=admin_user,
                    customer=customer,
                    total_amount=0,
                    date=timezone.now()
                )
                
                # Add items to sale
                for j in range(2):
                    product = products[i + j]
                    quantity = 2 + j
                    sale_item = SaleItem.objects.create(
                        sale=sale,
                        product=product,
                        quantity=quantity,
                        price=product.price
                    )
                    sale.total_amount += Decimal(str(sale_item.get_total()))
                
                sale.save()
                self.stdout.write(f'  ✓ Created sale #{sale.id} for {customer.name}')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created successfully!'))
