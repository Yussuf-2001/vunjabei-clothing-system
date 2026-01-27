from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from django.utils import timezone
from .models import Product, Customer, Sale, SaleItem, Category
from .serializers import (
    CategorySerializer, ProductSerializer, CustomerSerializer,
    SaleSerializer, SaleDetailSerializer, SaleItemSerializer
)


# ==================== API VIEWSETS ====================


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        if category_id:
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        products = Product.objects.filter(quantity__lt=10)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.query_params.get('q', '')
        customers = Customer.objects.filter(name__icontains=q) | Customer.objects.filter(phone__icontains=q)
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SaleDetailSerializer
        return SaleSerializer

    @action(detail=False, methods=['get'])
    def today_sales(self, request):
        today = timezone.now().date()
        sales = Sale.objects.filter(date__date=today)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        total_sales = Sale.objects.count()
        total_amount = sum(s.total_amount for s in Sale.objects.all())
        return Response({'total_sales': total_sales, 'total_amount': float(total_amount)})



@login_required
def dashboard(request):
    """Dashboard - Display statistics"""
    try:
        total_products = Product.objects.count()
        total_customers = Customer.objects.count()
        total_sales = Sale.objects.count()
        total_amount = sum(sale.total_amount for sale in Sale.objects.all())
    except:
        total_products = 0
        total_customers = 0
        total_sales = 0
        total_amount = 0
    
    recent_sales = Sale.objects.all()[:5]
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_sales': total_sales,
        'total_amount': total_amount,
        'recent_sales': recent_sales,
    }
    return render(request, 'clothing/dashboard.html', context)


@login_required
def product_list(request):
    """List all products"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'clothing/product_list.html', context)


@login_required
def product_create(request):
    """Create new product"""
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
        try:
            category = Category.objects.get(id=category_id) if category_id else None
            Product.objects.create(
                name=name,
                category=category,
                price=price,
                quantity=quantity
            )
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    categories = Category.objects.all()
    return render(request, 'clothing/product_form.html', {'categories': categories})


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'clothing/category_list.html', {'categories': categories})


@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            Category.objects.create(name=name)
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    return render(request, 'clothing/category_form.html')


@login_required
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all()
    return render(request, 'clothing/customer_list.html', {'customers': customers})


@login_required
def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        try:
            Customer.objects.create(
                name=name,
                phone=phone,
                address=address
            )
            messages.success(request, 'Customer created successfully!')
            return redirect('customer_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'clothing/customer_form.html')


@login_required
def sale_list(request):
    """List all sales"""
    sales = Sale.objects.all()
    return render(request, 'clothing/sale_list.html', {'sales': sales})


@login_required
def sale_create(request):
    """Create new sale"""
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        
        try:
            customer = Customer.objects.get(id=customer_id) if customer_id else None
            sale = Sale.objects.create(
                user=request.user,
                customer=customer,
                total_amount=0
            )
            messages.success(request, 'Sale created! Now add items.')
            return redirect('sale_detail', pk=sale.pk)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    customers = Customer.objects.all()
    return render(request, 'clothing/sale_form.html', {'customers': customers})


@login_required
def sale_detail(request, pk):
    """Sale detail with items"""
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        
        try:
            product = Product.objects.get(id=product_id)
            
            # Check stock
            if product.quantity < int(quantity):
                messages.error(request, 'Insufficient stock!')
                return redirect('sale_detail', pk=pk)
            
            # Create sale item
            sale_item = SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=int(quantity),
                price=product.price
            )
            
            # Update product quantity
            product.quantity -= int(quantity)
            product.save()
            
            # Update sale total
            # get_total() now returns a Decimal
            sale.total_amount += sale_item.get_total()
            sale.save()
            
            messages.success(request, 'Item added to sale!')
            return redirect('sale_detail', pk=pk)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    products = Product.objects.all()
    context = {
        'sale': sale,
        'items': sale.items.all(),
        'products': products,
    }
    return render(request, 'clothing/sale_detail.html', context)