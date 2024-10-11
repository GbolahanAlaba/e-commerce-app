from django.contrib import admin
from App_Commerce.models import *


@admin.register(Cart)
class Cartdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'date_created', 'date_modified']
    list_filter = ['user', 'date_created']
    search_fields = ['user']
    ordering = ['-date_created']

@admin.register(CartItem)
class CartItemdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'sub_total', 'cart', 'date_created', 'date_modified']
    list_filter = ['product', 'date_created']
    search_fields = ['product']
    ordering = ['-date_created']


@admin.register(Review)
class Reviewadmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'comment', 'date_created', 'date_modified']
    list_filter = ['user']
    search_fields = ['user']
    ordering = ['-date_created']


@admin.register(Order)
class Orderadmin(admin.ModelAdmin):
    list_display = ['user', 'get_products', 'total_price', 'order_date', 'reference', 'payment_status', 'delivery_status']
    list_filter = ['user']
    search_fields = ['user']
    ordering = ['-date_created']

    def get_products(self, obj):
        return ", ".join([f"{op.product.name} (x{op.quantity})" for op in obj.order_products.all()])
    get_products.short_description = 'Products'

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price', 'cost_price', 'discount_price', 'date_created']
    list_filter = ['order', 'product']
    search_fields = ['order__user__username', 'product__name']
    ordering = ['-date_created']


@admin.register(OrderReview)
class OrderReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'rating', 'comment', 'date_created', 'date_modified']
    list_filter = ['user']
    search_fields = ['user']
    ordering = ['-date_created']