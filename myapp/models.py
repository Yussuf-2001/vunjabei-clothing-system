from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from decimal import Decimal


# 1. Category Model
class Category(models.Model):
    """
    Model for product categories (e.g., T-shirts, Trousers, Shoes).
    """
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# 2. Product Model
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['name']), models.Index(fields=['category'])]

    def save(self, *args, **kwargs):
        """Make sure we never store a full URL in ``image.name``.

        When CloudinaryStorage is enabled the underlying library sometimes
        returns the *url* instead of the path portion and the field ends up
        containing a value like:

            https://res.cloudinary.com/…/image/upload/product_images/foo

        The storage backend in turn concatenates ``MEDIA_URL`` with this
        string, producing a doubled URL which can't be fetched from the
        browser.  This helper normalizes the name before committing it to the
        database:

        * strip any occurrence of ``MEDIA_URL`` prefix
        * if the name still begins with ``http`` cut everything up to the
          ``/upload/`` section (Cloudinary always exposes the object key after
          that path)
        """
        if self.image and self.image.name:
            from django.conf import settings

            media = settings.MEDIA_URL or ''
            if media and self.image.name.startswith(media):
                self.image.name = self.image.name[len(media) :]

            if self.image.name.startswith('http'):
                # look for the cloudinary upload divider and keep the part
                # after it, which is what storage expects as the ``name``.
                idx = self.image.name.find('/upload/')
                if idx != -1:
                    self.image.name = self.image.name[idx + len('/upload/') :]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# 3. Customer Model
class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


# 4. Sale Model
class Sale(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Sale #{self.pk} on {self.date.strftime('%Y-%m-%d')}"


# 5. SaleItem Model (Line items for a sale)
class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT) # Don't delete product if it's in a sale
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def get_total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    address = models.TextField(blank=True, null=True, help_text="Delivery Address / Maelekezo ya kufika")
    phone = models.CharField(max_length=20, blank=True, null=True, help_text="Contact Phone Number")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def save(self, *args, **kwargs):
        if self.product and self.quantity:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} ({self.status})"