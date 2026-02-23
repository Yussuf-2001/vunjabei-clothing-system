from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Customer, Order, Product, Sale
from .serializers import (
    CategorySerializer,
    CustomerSerializer,
    ProductSerializer,
    SaleDetailSerializer,
    SaleSerializer,
    UserRegistrationSerializer,
)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


def resolve_request_user(request):
    if getattr(request, 'user', None) and request.user.is_authenticated:
        return request.user

    username = ''
    if request.method in {'POST', 'PUT', 'PATCH'}:
        username = (request.data.get('username') or '').strip()
    if not username:
        username = (request.query_params.get('username') or '').strip()

    if not username:
        return None
    return User.objects.filter(username__iexact=username).first()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category_id = request.query_params.get('category_id')
        queryset = self.queryset
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        products = self.queryset.filter(quantity__lt=10)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])
        customers = Customer.objects.filter(name__icontains=query) | Customer.objects.filter(phone__icontains=query)
        serializer = self.get_serializer(customers.distinct(), many=True)
        return Response(serializer.data)


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().select_related('user', 'customer')
    serializer_class = SaleSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SaleDetailSerializer
        return SaleSerializer

    @action(detail=False, methods=['get'])
    def today_sales(self, request):
        today = timezone.now().date()
        sales = self.queryset.filter(date__date=today)
        serializer = self.get_serializer(sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        total_sales = self.queryset.count()
        total_amount = self.queryset.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        return Response({'total_sales': total_sales, 'total_amount': float(total_amount)})


class DashboardStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        total_products = Product.objects.count()
        total_customers = Customer.objects.count()

        today = timezone.now().date()
        today_sales = Sale.objects.filter(date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        low_stock_products = Product.objects.filter(quantity__lt=10)
        low_stock_items = list(low_stock_products.values('id', 'name', 'quantity'))

        recent_sales = Sale.objects.select_related('customer').order_by('-date')[:5]
        recent_sales_data = SaleSerializer(recent_sales, many=True).data

        return Response({
            'total_products': total_products,
            'total_customers': total_customers,
            'today_sales': float(today_sales),
            'low_stock_count': low_stock_products.count(),
            'low_stock_items': low_stock_items,
            'recent_sales': recent_sales_data,
        })


class PlaceOrderView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = resolve_request_user(request)
        if not user:
            return Response({'error': 'Login required to place order.'}, status=status.HTTP_403_FORBIDDEN)

        product_id = request.data.get('product_id')
        quantity_raw = request.data.get('quantity', 1)
        phone = request.data.get('phone')
        address = request.data.get('address')

        if not product_id:
            return Response({'error': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quantity = int(quantity_raw)
            if quantity <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({'error': 'Quantity must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                product = Product.objects.select_for_update().get(pk=product_id)

                if product.quantity < quantity:
                    return Response({'error': 'Insufficient stock for this product.'}, status=status.HTTP_400_BAD_REQUEST)

                order = Order.objects.create(
                    product=product,
                    user=user,
                    quantity=quantity,
                    total_price=product.price * quantity,
                    phone=phone,
                    address=address,
                )

                product.quantity -= quantity
                product.save(update_fields=['quantity'])

            return Response({'success': 'Order placed successfully.', 'order_id': order.id}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_health(request):
    return Response({'status': 'ok', 'service': 'vunjabei-api'})


@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([permissions.AllowAny])
def api_orders(request):
    user = resolve_request_user(request)
    if not user or not user.is_staff:
        return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    orders = Order.objects.select_related('user', 'product').order_by('-date_ordered')
    data = [
        {
            'id': order.id,
            'customer': order.user.username if order.user else 'Guest',
            'product_name': order.product.name if order.product else 'Unknown Product',
            'quantity': order.quantity,
            'total_price': float(order.total_price or 0),
            'status': order.status,
            'date': order.date_ordered.strftime('%Y-%m-%d %H:%M'),
            'phone': order.phone,
            'address': order.address,
        }
        for order in orders
    ]
    return Response(data)


@api_view(['POST'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([permissions.AllowAny])
def api_update_order_status(request, pk):
    user = resolve_request_user(request)
    if not user or not user.is_staff:
        return Response({'error': 'Admin access required.'}, status=status.HTTP_403_FORBIDDEN)

    order = get_object_or_404(Order, pk=pk)
    new_status = request.data.get('status')
    valid_statuses = {choice[0] for choice in Order.STATUS_CHOICES}

    if not new_status:
        return Response({'error': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)
    if new_status not in valid_statuses:
        return Response({'error': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)

    order.status = new_status
    order.save(update_fields=['status'])
    return Response({'message': 'Status updated successfully.'})


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def api_register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data = serializer.validated_data
    username = str(validated_data.get('username', '')).strip()
    email = str(validated_data.get('email', '')).strip()
    password = str(validated_data.get('password', '')).strip()

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    Customer.objects.create(name=user.username, email=user.email)

    return Response({'success': 'Registration successful. Please login.'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def api_register_staff(request):
    username = (request.data.get('username') or '').strip()
    email = (request.data.get('email') or '').strip()
    password = (request.data.get('password') or '').strip()

    if not username or not password:
        return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_staff = True
    user.is_superuser = False
    user.save(update_fields=['is_staff', 'is_superuser'])

    return Response({'success': 'Admin registration successful. Please login.'}, status=status.HTTP_201_CREATED)


@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def api_login(request):
    username = (request.data.get('username') or '').strip()
    password = (request.data.get('password') or '').strip()

    if not User.objects.filter(username=username).exists():
        return Response({'error': 'User does not exist. Please register first.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Incorrect password.'}, status=status.HTTP_400_BAD_REQUEST)

    auth_login(request, user)
    return Response({'username': user.username, 'is_staff': user.is_staff})


@api_view(['GET'])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([permissions.AllowAny])
def api_user_orders(request):
    user = resolve_request_user(request)
    if not user:
        return Response({'error': 'Login required.'}, status=status.HTTP_403_FORBIDDEN)

    orders = Order.objects.filter(user=user).select_related('product').order_by('-date_ordered')
    data = [
        {
            'id': order.id,
            'product_name': order.product.name,
            'quantity': order.quantity,
            'total_price': float(order.total_price or 0),
            'status': order.status,
            'date': order.date_ordered.strftime('%Y-%m-%d %H:%M'),
        }
        for order in orders
    ]
    return Response(data)
