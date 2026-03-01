from rest_framework import serializers
from .models import Category, Product, Customer, Sale, SaleItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'category_name',
            'price',
            'quantity',
            'image',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_image(self, obj):
        """Return a fully qualified URL for the product image.

        This method also repairs several mis‑formatted values we have seen in
        production:

        * ``url`` coming back from storage sometimes contains the full
          Cloudinary URL instead of just the path.  When ``MEDIA_URL`` is
          prepended to that the result is a broken double‑prefix string.
        * a valid Cloudinary URL may be missing the second slash after the
          ``https:`` scheme (``https:/…``); such strings are treated as
          relative by ``build_absolute_uri`` and get garbled further.

        The normalization below ensures the client always receives a usable
        https:// URL.
        """
        if not obj.image:
            return None

        try:
            url = obj.image.url
        except Exception:
            return None

        # drop accidental MEDIA_URL duplication
        from django.conf import settings

        media = settings.MEDIA_URL or ''
        if media and url.startswith(media) and url.count(media) > 1:
            # take the last occurrence and re‑prefix correctly
            url = media + url.split(media)[-1].lstrip('/')

        # fix missing slash after scheme
        if url.startswith('https:/') and not url.startswith('https://'):
            url = url.replace('https:/', 'https://', 1)

        request = self.context.get('request')
        if request:
            # only call build_absolute_uri for truly relative paths
            if not url.startswith('http'):
                return request.build_absolute_uri(url)
            return url

        # no request available – mimic DRF's normal behaviour
        if not url.startswith('http'):
            if media.endswith('/') and url.startswith('/'):
                url = url[1:]
            url = media + url.lstrip('/')
        elif url.startswith('http:'):
            url = url.replace('http:', 'https:')

        return url


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'address', 'created_at']
        read_only_fields = ['created_at']


class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total']

    def get_total(self, obj):
        return obj.get_total()


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True, allow_null=True)

    class Meta:
        model = Sale
        fields = ['id', 'user', 'user_name', 'customer', 'customer_name', 'date', 'total_amount', 'items']
        read_only_fields = ['date']


class SaleDetailSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'user', 'customer', 'date', 'total_amount', 'items']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
