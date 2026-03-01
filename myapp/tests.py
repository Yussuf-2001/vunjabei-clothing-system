from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from rest_framework.test import APIClient, APIRequestFactory
from .models import Category, Product
from .serializers import ProductSerializer
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


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.category = Category.objects.create(name="Hats")
        self.product = Product.objects.create(
            name="Cap",
            category=self.category,
            price=Decimal('10.00'),
            quantity=5,
        )
        # put a dummy image file (content doesn't matter)
        self.product.image.save(
            'cap.jpg', ContentFile(b'fakeimagecontent'), save=True
        )

    def test_image_url_serialization(self):
        """Serializer should return a fully-qualified URL for the image"""
        request = self.factory.get('/')
        serializer = ProductSerializer(self.product, context={'request': request})
        data = serializer.data
        self.assertIsNotNone(data.get('image'))
        # should start with either http or https or /media
        self.assertTrue(
            data['image'].startswith('http') or data['image'].startswith('/'),
            f"unexpected image url {data['image']}"
        )

    def test_serializer_fixes_double_prefix(self):
        """Even if storage returns a mangled URL, serializer cleans it."""
        bad_url = 'https:/res.cloudinary.com/foo/image/upload/product_images/x'
        # monkeypatch the product's url property
        class Dummy:
            url = bad_url
        self.product.image = Dummy()
        request = self.factory.get('/')
        data = ProductSerializer(self.product, context={'request': request}).data
        self.assertEqual(data['image'], 'https://res.cloudinary.com/foo/image/upload/product_images/x')

    def test_save_strips_full_url_from_name(self):
        """Product.save() removes MEDIA_URL or http prefix from image name."""
        from django.conf import settings
        p = Product(
            name='Foo',
            category=self.category,
            price=Decimal('1.00'),
            quantity=1,
        )
        # simulate an incorrectly stored name (full cloudinary url)
        p.image.name = settings.MEDIA_URL + 'https:/res.cloudinary.com/foo/image/upload/product_images/bar'
        p.save()
        self.assertFalse(p.image.name.startswith('http'))
        self.assertFalse(p.image.name.startswith(settings.MEDIA_URL))


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
