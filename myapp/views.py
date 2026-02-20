from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.views.decorators.http import require_http_methods
from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum
from django.db import transaction
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Product, Customer, Sale, SaleItem, Category, Order
from .forms import OrderForm
from .serializers import (
    CategorySerializer, ProductSerializer, CustomerSerializer,
    SaleSerializer, SaleDetailSerializer, SaleItemSerializer,
    UserRegistrationSerializer
)


# ==================== API VIEWSETS ====================


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

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
        total_amount = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        return Response({'total_sales': total_sales, 'total_amount': float(total_amount or 0)})


class PlaceOrderView(APIView):
    """
    API ya kupokea oda kutoka React.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        phone = request.data.get('phone')
        address = request.data.get('address')

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=product_id)

                if product.quantity < quantity:
                    return Response({'error': 'Samahani, bidhaa hii imeisha au haitoshi.'}, status=status.HTTP_400_BAD_REQUEST)

                # Tumia user aliye-login kutoka kwenye request. Hii ni salama zaidi.
                user = request.user
                order = Order.objects.create(
                    product=product,
                    user=user,
                    quantity=quantity,
                    total_price=product.price * quantity,
                    phone=phone,
                    address=address
                )

                product.quantity -= quantity
                product.save()

            return Response({'success': 'Order placed successfully!', 'order_id': order.id}, status=status.HTTP_201_CREATED)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def api_register(request):
    """API ya kusajili Customer kupitia React"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        # Tunatengeneza user wa kawaida (sio staff)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=serializer.validated_data['password']
        )
        # Pia tunamtengenezea Customer profile
        Customer.objects.create(name=user.username)
        return Response({'success': 'Usajili umekamilika! Tafadhali login.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def api_login(request):
    """API ya Login kwa React"""
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        return Response({'success': True, 'username': user.username, 'id': user.id})
    return Response({'error': 'Jina au nenosiri sio sahihi'}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def dashboard(request):
    """Dashboard - Display statistics"""
    # Redirect non-staff users (Customers) to the product list
    if not request.user.is_staff:
        return redirect('product_list')

    try:
        total_products = Product.objects.count()
        total_customers = Customer.objects.count()
        total_sales = Sale.objects.count()
        total_amount = Sale.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_orders = Order.objects.count()
    except:
        total_products = 0
        total_customers = 0
        total_sales = 0
        total_amount = 0
        total_orders = 0
    
    recent_sales = Sale.objects.all()[:5]
    recent_sales = Sale.objects.order_by('-date')[:5]
    
    context = {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_sales': total_sales,
        'total_amount': total_amount,
        'total_orders': total_orders,
        'recent_sales': recent_sales,
    }
    return render(request, 'myapp/dashboard.html', context)


@login_required
def product_list(request):
    """List all products"""
    products = Product.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
        
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    
    # Pagination (Show 12 products per page)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'myapp/product_list.html', context)


@login_required
def product_create(request):
    """Create new product"""
    if request.method == 'POST':
        return save_product(request)
    
    categories = Category.objects.all()
    return render(request, 'myapp/product_form.html', {'categories': categories})

def save_product(request, product=None):
    """Helper to save product (used for create and update)"""
    try:
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        
        category = Category.objects.get(id=category_id) if category_id else None
        
        # Clean price input (remove commas)
        price_clean = price.replace(',', '') if price else '0'

        # Validate inputs
        if float(price_clean) < 0 or int(quantity) < 0:
            messages.error(request, 'Price and Quantity must be positive!')
            return render(request, 'myapp/product_form.html', {'categories': Category.objects.all(), 'product': product})
            
        if product:
            # Update existing
            product.name = name
            product.category = category
            product.price = float(price_clean)
            product.quantity = int(quantity)
            if image:
                product.image = image
            product.save()
            messages.success(request, 'Product updated successfully!')
        else:
            # Create new
            Product.objects.create(
                name=name,
                category=category,
                price=float(price_clean),
                quantity=int(quantity),
                image=image
            )
            messages.success(request, 'Product created successfully!')
        return redirect('product_list')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return render(request, 'myapp/product_form.html', {'categories': Category.objects.all(), 'product': product})

@login_required
def product_update(request, pk):
    """Edit existing product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        return save_product(request, product)
    categories = Category.objects.all()
    return render(request, 'myapp/product_form.html', {'categories': categories, 'product': product})

@login_required
def product_delete(request, pk):
    """Delete product"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'myapp/product_confirm_delete.html', {'product': product})


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'myapp/category_list.html', {'categories': categories})


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
    return render(request, 'myapp/category_form.html')


@login_required
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.all()
    return render(request, 'myapp/customer_list.html', {'customers': customers})


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
    
    return render(request, 'myapp/customer_form.html')


@login_required
def sale_list(request):
    """List all sales"""
    sales = Sale.objects.all()
    return render(request, 'myapp/sale_list.html', {'sales': sales})


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
    return render(request, 'myapp/sale_form.html', {'customers': customers})


@login_required
def sale_detail(request, pk):
    """Sale detail with items"""
    sale = get_object_or_404(Sale, pk=pk)
    
    if request.method == 'POST':
        product_id = request.POST.get('product')
        quantity = request.POST.get('quantity')
        
        try:
            qty = int(quantity)
            if qty <= 0:
                messages.error(request, 'Quantity must be positive!')
                return redirect('sale_detail', pk=pk)

            product = Product.objects.get(id=product_id)
            
            # Check stock
            if product.quantity < qty:
                messages.error(request, 'Insufficient stock!')
                return redirect('sale_detail', pk=pk)
            
            # Create sale item
            sale_item = SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=qty,
                price=product.price
            )
            
            # Update product quantity
            product.quantity -= qty
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
    return render(request, 'myapp/sale_detail.html', context)


@login_required
def sale_remove_item(request, sale_id, item_id):
    """Remove item from sale and restore stock"""
    sale = get_object_or_404(Sale, pk=sale_id)
    item = get_object_or_404(SaleItem, pk=item_id, sale=sale)
    
    try:
        # Restore stock
        product = item.product
        product.quantity += item.quantity
        product.save()
        
        # Update sale total
        sale.total_amount -= item.get_total()
        if sale.total_amount < 0:
            sale.total_amount = 0
        sale.save()
        
        item.delete()
        messages.success(request, 'Item removed from sale.')
    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')
        
    return redirect('sale_detail', pk=sale_id)


@login_required
def profile(request):
    """User profile page"""
    return render(request, 'myapp/profile.html')


def register(request):
    """Register a new Admin/Staff user (Inatumika na Django Admin pekee)"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True  # Hii ni MUHIMU: Inamfanya user huyu awe Admin/Staff
            user.save()
            auth_login(request, user)
            messages.success(request, 'Admin Registration successful!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def user_logout(request):
    """Logout user and redirect to login page"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('user_login')

@login_required
def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.user = request.user
            
            # Check if enough stock exists
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                product.save()
                order.save()
                messages.success(request, f'Successfully ordered {product.name}!')
                return redirect('order_list')
            else:
                messages.error(request, 'Not enough stock available.')
    else:
        form = OrderForm()

    return render(request, 'myapp/order_form.html', {
        'form': form,
        'product': product
    })

@login_required
def order_list(request):
    """List orders placed by the current user"""
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'myapp/order_list.html', {'orders': orders})

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_user_orders(request):
    """API ya kuonyesha oda za mteja kwenye React"""
    # Tunavuta oda za user aliye-login PEKEE (Usalama)
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'product_name': order.product.name,
            'quantity': order.quantity,
            'total_price': order.total_price,
            'status': order.status,
            'date': order.date_ordered.strftime("%Y-%m-%d %H:%M"),
        })
    return Response(data)


@login_required
def manage_orders(request):
    """Admin view to see and manage all customer orders."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('dashboard')

    orders = Order.objects.all().order_by('-date_ordered')
    
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)

    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'myapp/manage_orders.html', context)


@login_required
@require_http_methods(["POST"])
def update_order_status(request, order_id):
    """Handles the POST request to update an order's status."""
    if not request.user.is_staff:
        return redirect('dashboard')

    order = get_object_or_404(Order, id=order_id)
    order.status = request.POST.get('status', order.status)
    order.save()
    messages.success(request, f"Order #{order.id} status updated to {order.status}.")
    return redirect('manage_orders')