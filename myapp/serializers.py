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
        
        # Get the full URL directly from the storage backend (Cloudinary or Local)
        if instance.image:
            try:
                url = instance.image.url
                request = self.context.get('request')
                # If URL is already absolute (Cloudinary), use it. Otherwise build it (Local).
                if url.startswith('http'):
                    representation['image'] = url
                elif request:
                    representation['image'] = request.build_absolute_uri(url)
                else:
                    representation['image'] = url
            except Exception:
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
