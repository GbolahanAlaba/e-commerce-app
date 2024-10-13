from django.contrib.auth.models import User
from . models import *
from rest_framework.response import Response
from rest_framework import serializers, validators
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import *
from drf_extra_fields.fields import Base64ImageField
from django.db.models import Count
from django.db.models import Avg, Count
from random import randint



class SubcategorySerializer(serializers.ModelSerializer):
    category_id = serializers.UUIDField(write_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ['subcategory_id', 'category_id', 'category', 'name']

    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
    
        try:
            category = Category.objects.get(category_id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist")
    
        subcategory = Subcategory.objects.create(category=category, **validated_data)
        return subcategory
    
    def get_category(self, obj):
        return f"{obj.category.name}"

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_id', 'name', 'description', 'subcategories']

    def create(self, validated_data):
        
        category = Category.objects.create(**validated_data)
        return category

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(required=False)

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

class UploadProductSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    product_images = serializers.ListField(
        child = Base64ImageField(max_length=1000000, allow_empty_file = True, use_url = False),
        write_only = True
        )

    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'subcategory', 'price', 'discount', 'quantity', 'weight', 'featured', 'top_deal', 'description', 'slug', 'images', 'product_images']

    def create(self, validated_data):
        product_images = validated_data.pop('product_images', [])

        pn = {'pn': 'PN'}
        product_no = "{}{}".format(pn ['pn'], randint(1000000, 9000000))
        
        product = Product.objects.create(**validated_data, product_no=product_no)
        for image in product_images:
            new_product_image = ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.price = validated_data.get('price', instance.price)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update product images if provided
        product_images_data = validated_data.get('product_images')
        if product_images_data:
            # Delete existing images
            instance.images.all().delete()
            # Create new images
            for image_data in product_images_data:
                ProductImage.objects.create(product=instance, image=image_data)
        return instance

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'category', 'subcategory', 'price', 'discount', 'weight', 'description', 'slug', 'images',]







# class CartItemSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CartItem
#         fields = ['id', 'product', 'quantity']

# class CartSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(read_only=True)
#     items = CartItemSerializer(many=True, read_only=True)
#     # calc_total_price = serializers.SerializerMethodField() # A special method in the serialzer

#     # def get_total_price(self, obj): # function for the special method "calc_total_price"
#     #     return obj.calc_total_price()
    
#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'items', 'total_price']

# # ORDERS
# class OrderProSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['name']

# class OrderProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = OrderProduct
#         fields = ['product', 'quantity', 'price']

# class OrderSerializer(serializers.ModelSerializer):
#     order_products = OrderProductSerializer(many=True, source='orderproduct_set')

#     class Meta:
#         model = Order
#         fields = ['id', 'user', 'order_products', 'total_price', 'order_date', 'shipping_address', 'shipping_method', 'payment_method', 'date_created']
#         read_only_fields = ['user', 'total_price', 'order_date', 'date_created']

#     def create(self, validated_data):
#         order_products_data = validated_data.pop('orderproduct_set')
#         user = validated_data.pop('user')

#         total_price = 0
#         for order_product_data in order_products_data:
#             total_price += order_product_data['price'] * order_product_data['quantity']

#         order = Order.objects.create(user=user, total_price=total_price, **validated_data)

#         for order_product_data in order_products_data:
#             OrderProduct.objects.create(order=order, **order_product_data)

#         return order

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         order_products = OrderProduct.objects.filter(order=instance)
#         representation['order_products'] = OrderProductSerializer(order_products, many=True).data
#         return representation

# class OrderRecordsSerializer(serializers.ModelSerializer):
#     products = OrderProSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = ['order_id', 'products', 'total_price', 'order_date', 'delivery_status', 'reference']

# class ProductSerializer_For_OrderInfo(serializers.ModelSerializer):
#     images = ProductImageSerializer(many=True, read_only=True)
#     # price = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = ['name', 'description', 'images']

#     # def get_price(self, obj):
#     #     order_product = self.context.get('order_product')
#     #     if order_product and order_product.product:
#     #         product = order_product.product
#     #         return product.discount if product.discount > 0.00 else product.price
#     #     return None

# class OrderSerializer_For_OrderInfo(serializers.ModelSerializer):
#     cost_price = serializers.SerializerMethodField()
#     discount_amount = serializers.SerializerMethodField()
#     total = serializers.SerializerMethodField()
    

#     class Meta:
#         model = Order
#         fields = ['order_id', 'payment_method', 'cost_price', 'discount_amount', 'total']

#     def get_cost_price(self, obj):
#         total_discount = OrderProduct.objects.filter(order=obj).aggregate(
#             total_cost=models.Sum(models.F('cost_price') * models.F('quantity'))
#         )['total_cost']
#         return total_discount if total_discount is not None else 0
    
#     def get_discount_amount(self, obj):
#         total_discount = OrderProduct.objects.filter(order=obj).aggregate(
#             total_discount=Sum(
#                 ExpressionWrapper(
#                     (F('cost_price') - F('discount_price')) * F('quantity'),
#                     output_field=DecimalField()
#                 )
#             )
#         )['total_discount']
#         return total_discount if total_discount is not None else 0
    
#     def get_total(self, obj):
#         total_cost_price = self.get_cost_price(obj)
#         total_discount = self.get_discount_amount(obj)
#         total = total_cost_price - total_discount
#         return total

# class OrderInfoSerializer(serializers.ModelSerializer):
#     product = ProductSerializer_For_OrderInfo(many=False, read_only=True)

#     class Meta:
#         model = OrderProduct
#         fields = ['id', 'product', 'price', 'quantity', 'sub_total']

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         self.fields['product'].context.update(self.context)
#         self.fields['product'].context['order_product'] = instance
#         return representation

# class CheckoutSerializer(serializers.Serializer):
#     wallet_balance = serializers.CharField()
#     total_item = serializers.IntegerField()
#     total_price = serializers.DecimalField(max_digits=10, decimal_places=2)
#     delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2)
#     service_charge = serializers.DecimalField(max_digits=10, decimal_places=2)
#     total = serializers.DecimalField(max_digits=10, decimal_places=2)