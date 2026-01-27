from rest_framework import serializers
from .models import Category, Product, Customer, Sale, SaleItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'price', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


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

from rest_framework import serializers
from .models import Category, Product, Customer, Sale, SaleItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name', 'price', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


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
