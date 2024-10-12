from django.db import models
from App_Auth.models import User
from datetime import date, datetime, timedelta
from django.utils import timezone
import uuid
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    description = models.CharField(max_length=100, blank=True, null=True, default="")
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return str(self.name)
    
class Subcategory(models.Model):
    subcategory_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, default="", related_name="subcategories")
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = "Subcategories"
    
class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True, default="")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, default="", related_name="product_categories")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, blank=True, null=True, default="", related_name="product_subcategories")
    price = models.DecimalField(max_digits=100, blank=True, null=False, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=100, blank=True, null=False, decimal_places=2, default=0.0)
    weight = models.CharField(max_length=100, blank=True, null=True, default=0)
    quantity = models.PositiveBigIntegerField(default=0)
    description = models.TextField(max_length=10000, blank=True, null=True, default="")
    image = models.ImageField(upload_to="product_images", blank=True, null=True, default="")
    featured = models.BooleanField(default=False)
    top_deal = models.BooleanField(default=False)
    product_no = models.CharField(max_length=100, blank=True, null=True, default="")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default="")
    slug = models.SlugField(max_length=250)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:  
            base_slug = slugify(self.name)
            unique_slug = base_slug
            count = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{get_random_string(length=4)}'
                count += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="product_images", blank=True, null=True, default="")
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.product)
    

# class Cart(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
#     session_key = models.CharField(max_length=100, null=True, blank=True)    
#     date_created = models.DateTimeField(default=timezone.now)
#     date_modified = models.DateTimeField(default=timezone.now)

#     def total_price(self):
#         total = sum(item.sub_total() for item in self.items.all())
#         # total = sum(item.product.price * item.quantity for item in self.items.all())
#         return total
    
#     def cart_items_count(self):
#         return self.items.values('product').distinct().count() # Count the distinct products in the cart
    
#     def __str__(self):
#         return f"{self.user}"

# class CartItem(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems')
#     quantity = models.PositiveBigIntegerField(default=0)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     date_created = models.DateTimeField(default=timezone.now)
#     date_modified = models.DateTimeField(default=timezone.now)

#     class Meta:
#         ordering = ['-date_created']
#         indexes = [models.Index(fields=['-date_created'])]

#     def sub_total(self):
#         sub_price =  self.product.price * self.quantity
#         sub_discount_price = self.product.discount * self.quantity
#         if sub_discount_price <= 0.00:
#             return int(sub_price)
#         else:
#             return int(sub_discount_price)
    
#     def count_quantity(self):
#         return self.quantity    
    
#     def save(self, *args, **kwargs):
#         if self.quantity > self.product.quantity:
#             raise ValueError(f"Cannot add {self.quantity} items of {self.product.name} to cart. Only {self.product.quantity} available.")
#         super().save(*args, **kwargs)

# class Order(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     order_id = models.CharField(max_length=50, unique=True)
#     products = models.ManyToManyField(Product, through='OrderProduct')
#     items_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     order_date = models.DateTimeField(auto_now_add=True)
#     shipping_address = models.TextField()
#     shipping_method = models.CharField(max_length=50)
#     payment_method = models.CharField(max_length=50)
#     payment_status = models.CharField(max_length=50, default="Pending")
#     delivery_status = models.CharField(max_length=50, default="Pending")
#     delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     reference = models.CharField(max_length=50, null=True, blank=True, default="Ref")
#     date_created = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return f"{self.order_id}"

# class OrderProduct(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
#     order_iid = models.CharField(max_length=50, default=1)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     cost_price = models.DecimalField(max_digits=10, decimal_places=2) # added for use
#     discount_price = models.DecimalField(max_digits=10, decimal_places=2) # added for use
#     date_created = models.DateTimeField(default=timezone.now)
    
#     def sub_total(self):
#         sub_price = self.price * self.quantity
#         return sub_price
    
#     def sub_total_cost_price(self):
#         return self.cost_price * self.quantity
    
#     def sub_total_discount_price(self):
#         return self.discount_price * self.quantity

#     def unit_price(self):
#         return self.product.calculate_discounted_price()
    
#     def __str__(self):
#         return f"{self.product}"
    
#     class Meta:
#         ordering = ['-date_created']
    
#     # def sub_total(self):
#     #     sub_price =  self.product.discount * self.quantity if self.product.discount else self.product.price * self.quantity
#     #     return sub_price


