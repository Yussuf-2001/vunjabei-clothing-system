from rest_framework import serializers
from .models import Category, Product, Customer, Sale, SaleItem
from django.contrib.auth.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'price', 'quantity', 'image', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def to_representation(self, instance):
        """Ensure image URL is absolute"""
        representation = super().to_representation(instance)
        
        if instance.image:
            try:
                # Get URL directly from storage backend (Cloudinary or Local)
                url = instance.image.url

                # SAFETY CHECK: If url is just a filename (e.g. "image.png"), prepend /media/
                if not url.startswith('http') and not url.startswith('/'):
                    url = f'/media/{url}'
                
                # If it's a relative path (local storage), make it absolute
                if url.startswith('/'):
                    request = self.context.get('request')
                    if request:
                        url = request.build_absolute_uri(url)
                # If it's external (Cloudinary) but http, force https
                elif url.startswith('http:'):
                    url = url.replace('http:', 'https:')
                
                representation['image'] = url
            except Exception:
                # If URL generation fails (e.g. missing file), return None
                representation['image'] = None
                
        return representation


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
