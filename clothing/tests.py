from django.test import TestCase
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
