from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'products', views.ProductViewSet, basename='product')
router.register(r'customers', views.CustomerViewSet, basename='customer')
router.register(r'sales', views.SaleViewSet, basename='sale')

urlpatterns = [
    path('health/', views.api_health, name='api_health'),
    path('dashboard-stats/', views.DashboardStatsView.as_view(), name='api_dashboard_stats'),
    path('place-order/', views.PlaceOrderView.as_view(), name='api_place_order'),
    path('register/', views.api_register, name='api_register'),
    path('register-staff/', views.api_register_staff, name='api_register_staff'),
    path('login/', views.api_login, name='api_login'),
    path('my-orders/', views.api_user_orders, name='api_user_orders'),
    path('orders/', views.api_orders, name='api_orders'),
    path('orders/<int:pk>/update-status/', views.api_update_order_status, name='api_update_order_status'),
    path('', include(router.urls)),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
