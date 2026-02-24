from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Category, Product
from decimal import Decimal

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="T-Shirts")

    def test_category_creation(self):
        """Test that a category is created correctly"""
        self.assertEqual(self.category.name, "T-Shirts")
        self.assertTrue(isinstance(self.category, Category))
        self.assertEqual(str(self.category), "T-Shirts")


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Jeans")
        self.product = Product.objects.create(
            name="Blue Denim",
            category=self.category,
            price=Decimal('25.00'),
            quantity=50
        )

    def test_product_creation(self):
        """Test that a product is created with correct attributes"""
        self.assertEqual(self.product.name, "Blue Denim")
        self.assertEqual(self.product.price, Decimal('25.00'))
        self.assertEqual(self.product.quantity, 50)
        self.assertEqual(self.product.category.name, "Jeans")

    def test_stock_management(self):
        """Test stock reduction logic"""
        initial_stock = self.product.quantity
        sold_quantity = 5
        
        # Simulate sale
        self.product.quantity -= sold_quantity
        self.product.save()
        
        self.assertEqual(self.product.quantity, initial_stock - sold_quantity)

    def test_low_stock_logic(self):
        """Test logic for identifying low stock"""
        self.product.quantity = 5
        self.product.save()
        self.assertTrue(self.product.quantity < 10)


class OrderApiAuthTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.customer_user = User.objects.create_user(username="customer1", password="pass12345")
        self.staff_user = User.objects.create_user(username="admin1", password="pass12345", is_staff=True)
        self.category = Category.objects.create(name="Sneakers")
        self.product = Product.objects.create(
            name="Air Runner",
            category=self.category,
            price=Decimal('100.00'),
            quantity=10,
        )

    def test_place_order_requires_authentication(self):
        response = self.client.post(
            '/api/place-order/',
            {'product_id': self.product.id, 'quantity': 1, 'phone': '0712345678', 'address': 'Dar'},
            format='json',
        )
        self.assertEqual(response.status_code, 403)

    def test_authenticated_user_can_place_order_and_stock_reduces(self):
        self.client.force_login(self.customer_user)
        response = self.client.post(
            '/api/place-order/',
            {'product_id': self.product.id, 'quantity': 2, 'phone': '0712345678', 'address': 'Dar'},
            format='json',
        )
        self.assertEqual(response.status_code, 201)

        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 8)

    def test_orders_endpoint_requires_staff(self):
        self.client.force_login(self.customer_user)
        response = self.client.get('/api/orders/')
        self.assertEqual(response.status_code, 403)

    def test_staff_can_access_orders_endpoint(self):
        self.client.force_login(self.customer_user)
        self.client.post(
            '/api/place-order/',
            {'product_id': self.product.id, 'quantity': 1, 'phone': '0712345678', 'address': 'Dar'},
            format='json',
        )

        self.client.logout()
        self.client.force_login(self.staff_user)
        response = self.client.get('/api/orders/')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(response.json(), list))
