from django.contrib import admin
from . models import *

def duplicate_records(modeladmin, request, queryset):
    for record in queryset:
        record.pk = None  # Set primary key to None to create a new record
        record.save()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'date_created', 'date_modified']
    list_filter = ['name', 'date_created']
    search_fields = ['name']
    ordering = ['-date_created']

@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'date_created', 'date_modified']
    list_filter = ['name', 'date_created']
    search_fields = ['name']
    ordering = ['-date_created']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'category', 'subcategory', 'price', 'discount', 'quantity', 'slug', 'featured', 'top_deal', 'date_created', 'date_modified']
    list_filter = ['name', 'category', 'date_created']
    search_fields = ['name', 'category', 'subcategory']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'date_created'
    ordering = ['-date_created']
    list_editable = ['description', 'category', 'subcategory', 'price', 'discount', 'quantity', 'slug', 'featured', 'top_deal',]
    list_display_links = ['name']
    actions = [duplicate_records]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'date_created']
    list_filter = ['product', 'date_created']
    list_editable = ['image']
    search_fields = ['product']
    ordering = ['-date_created']

    
# @admin.register(Cart)
# class Cartdmin(admin.ModelAdmin):
#     list_display = ['user', 'session_key', 'date_created', 'date_modified']
#     list_filter = ['user', 'date_created']
#     search_fields = ['user']
#     ordering = ['-date_created']

# @admin.register(CartItem)
# class CartItemdmin(admin.ModelAdmin):
#     list_display = ['product', 'quantity', 'sub_total', 'cart', 'date_created', 'date_modified']
#     list_filter = ['product', 'date_created']
#     search_fields = ['product']
#     ordering = ['-date_created']


# @admin.register(Review)
# class Reviewadmin(admin.ModelAdmin):
#     list_display = ['user', 'product', 'rating', 'comment', 'date_created', 'date_modified']
#     list_filter = ['user']
#     search_fields = ['user']
#     ordering = ['-date_created']


# @admin.register(Order)
# class Orderadmin(admin.ModelAdmin):
#     list_display = ['user', 'get_products', 'total_price', 'order_date', 'reference', 'payment_status', 'delivery_status']
#     list_filter = ['user']
#     search_fields = ['user']
#     ordering = ['-date_created']

#     def get_products(self, obj):
#         return ", ".join([f"{op.product.name} (x{op.quantity})" for op in obj.order_products.all()])
#     get_products.short_description = 'Products'

# @admin.register(OrderProduct)
# class OrderProductAdmin(admin.ModelAdmin):
#     list_display = ['order', 'product', 'quantity', 'price', 'cost_price', 'discount_price', 'date_created']
#     list_filter = ['order', 'product']
#     search_fields = ['order__user__username', 'product__name']
#     ordering = ['-date_created']


# @admin.register(OrderReview)
# class OrderReviewAdmin(admin.ModelAdmin):
#     list_display = ['user', 'order', 'rating', 'comment', 'date_created', 'date_modified']
#     list_filter = ['user']
#     search_fields = ['user']
#     ordering = ['-date_created']