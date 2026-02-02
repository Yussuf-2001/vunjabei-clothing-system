from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static

# API Router
router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'sales', views.SaleViewSet, basename='sale')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Authentication
    path('accounts/login/', RedirectView.as_view(url='/login/')),
    path('accounts/logout/', views.user_logout, name='logout_alt'),
    path('login/', auth_views.LoginView.as_view(next_page='dashboard', template_name='clothing/login.html'), name='user_login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('order/create/<int:product_id>/', views.order_create, name='order_create'),
    path('my-orders/', views.order_list, name='order_list'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    
    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/create/', views.customer_create, name='customer_create'),
    
    # Sales
    path('sales/', views.sale_list, name='sales'),
    path('sales/create/', views.sale_create, name='sale_create'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:sale_id>/remove_item/<int:item_id>/', views.sale_remove_item, name='sale_remove_item'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)