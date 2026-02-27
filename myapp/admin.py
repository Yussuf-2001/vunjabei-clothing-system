from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Category, Product, Customer, Sale, SaleItem, Order


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'quantity', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'category', 'price', 'quantity', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'address', 'created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at']
    fieldsets = (
        ('Customer Info', {
            'fields': ('name', 'phone', 'address')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    fields = ['product', 'quantity', 'price']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'user', 'total_amount', 'date']
    list_filter = ['date', 'user']
    readonly_fields = ['date', 'total_amount']
    inlines = [SaleItemInline]
    fieldsets = (
        ('Sale Info', {
            'fields': ('user', 'customer', 'date', 'total_amount')
        }),
    )
    
    def customer_name(self, obj):
        return obj.customer.name if obj.customer else 'Walk-in'
    customer_name.short_description = 'Customer'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'sale', 'product', 'quantity', 'price', 'get_total']
    list_filter = ['sale', 'product']
    search_fields = ['product__name']
    readonly_fields = ['get_total']
    
    def get_total(self, obj):
        return f"${obj.get_total():.2f}"
    get_total.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'phone', 'quantity', 'total_price', 'status', 'date_ordered']
    list_filter = ['status', 'date_ordered']
    search_fields = ['user__username', 'phone', 'product__name']
    list_editable = ['status']


# Re-register UserAdmin to show staff status clearly
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)