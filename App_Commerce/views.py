from django.http import JsonResponse
from django.shortcuts import render

from . models import *
from . serializers import *
from . serializers import *
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, status
from rest_framework import status
from knox.auth import TokenAuthentication
from random import randint
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.db import IntegrityError
from urllib.parse import quote, unquote
from django.contrib.sessions.models import Session
from functools import wraps
from django.db.models import Avg
import math
from rest_framework.decorators import action



# class CategoryViewSets(viewsets.ViewSet):
#     serializer_class = CategorySerializer

#     @handle_exceptions
#     def list_categories(self, request):
#         categories = Category.objects.all().order_by("date_created")

#         serializer = self.serializer_class(categories, many=True)

#         category_data = []
#         for category in serializer.data:
#             selected_fields = {
#                 'id': category.get('id'),
#                 'name': category.get('category'),
#                 'description': category.get('description'),
#                 'image': category.get('images'),              
#             }
#             category_data.append(selected_fields)
        
#         return Response({"status": "success", "message": "All categories", "data": category_data}, status=status.HTTP_200_OK)
    
#     @handle_exceptions
#     def categories_and_subcategories(self, request):
#         cache_key = 'categories_and_subcategories'
#         category_data = cache.get(cache_key)
#         source = "cache" if category_data else "database"

#         if not category_data:
#             cat = Category.objects.all().order_by("date_created")
#             serializer = self.serializer_class(cat, many=True)
#             category_data = [
#                 {
#                     'id': category['id'],
#                     'category': category['category'],
#                     'subcategories': [
#                         {
#                             'id': subcat['id'],
#                             'subcategory': subcat['subcategory']
#                         }
#                         for subcat in category.get('subcategories', [])
#                     ]
#                 }
#                 for category in serializer.data
#             ]
#             cache.set(cache_key, category_data, 60 * 60)  # Cache for 60 minutes
#         # return Response({"status": "success", "message": "Categories and their subcategories", "data": category_data}, status=status.HTTP_200_OK)
#         response = Response({"status": "success", "message": "Categories and their subcategories", "data": category_data}, status=status.HTTP_200_OK)
#         response['X-Cache-Source'] = source  # Add custom header indicating source
#         return response
    
    
#     @handle_exceptions
#     def category_and_subcategories(self, request, category_id):
#         cache_key = 'category_and_subcategories'
#         category_data = cache.get(cache_key)

#         if not category_data:
#             cat = Category.objects.filter(id=category_id).first()

#             serializer = self.serializer_class(cat)
#             category_data = {
#             'id': serializer.data.get('id'),
#             'category_name': serializer.data.get('category'),
#             'subcategories': [
#                 {
#                     'id': subcat.get('id'),
#                     'name': subcat.get('subcategory')
#                 }
#                 for subcat in serializer.data.get('subcategories', [])
#                 ]
#             }
#             cache.set(cache_key, category_data, 60 * 60)
        
#         return Response({"status": "success", "message": f"{cat.category} subcategories", "data": category_data}, status=status.HTTP_200_OK)
    
#     def delete_cache(self, request):
#         cache_key = 'featured_products'
#         cache.delete(cache_key)
#         return Response({"status": "success", "message": "Cache cleared successfully"}, status=status.HTTP_200_OK)

# class SubCategoryViewSets(viewsets.ViewSet):
#     serializer_class = SubcategorySerializer
    
#     @handle_exceptions
#     def list_subcategories(self, request, *args, **kwargs):
#         subcategories = Subcategory.objects.all()

#         serializer = self.serializer_class(subcategories, many=True)

#         subcategories_data = [
#             {
#                 "id": subcategory["id"],
#                 "category": subcategory["category"],
#                 "subcategory_name": subcategory["subcategory"],
#             }
#                 for subcategory in serializer.data
#         ]

#         return Response({"status": "success", "message": "All Subcategories.", "data": subcategories_data}, status=status.HTTP_200_OK)

# class ProductsViewSet(viewsets.ViewSet):
#     serializer_class = ProductSerializer

#     @handle_exceptions
#     def all_products(self, request, *args, **kwargs):
#         queryset = Product.objects.all().order_by("-date_created")
#         serializer = self.serializer_class(queryset, many=True)

#         product_data = []
#         for product in serializer.data:
#             # images = [{"product": product.get('name'), "images": img['image']} for img in product.get('images', [])]
#             product_ins = Product.objects.get(id=product['id'])
#             average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#             rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#             selected_fields = {
#                 'id': product.get('id'),
#                 'name': product.get('name'),
#                 'price': product.get('price'),
#                 'discount': product.get('discount'),
#                 'reviews': rounded_average_rating,
#                 'images': product.get('images')                     
#             }
#             product_data.append(selected_fields)
        
#         return Response({"status": "success", "message": "All products.", "data": product_data}, status=status.HTTP_200_OK)
    
#     @handle_exceptions
#     def featured_products(self, request, *args, **kwargs):
#         cache_key = 'featured_products'
#         product_data = cache.get(cache_key)
#         source = "cache" if product_data else "database"

#         if not product_data:
#             queryset = Product.objects.filter(featured=True).order_by("-date_created")
#             serializer = self.serializer_class(queryset, many=True)
#             product_data = []

#             for product in serializer.data:
#                 product_ins = Product.objects.get(id=product['id'])
#                 average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#                 rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#                 selected_fields = {
#                     'id': product.get('id'),
#                     'name': product.get('name'),
#                     'price': product.get('price'),
#                     'discount': product.get('discount'),
#                     'reviews': rounded_average_rating,
#                     'images': product.get('images')
#                 }
#                 product_data.append(selected_fields)

#             cache.set(cache_key, product_data, 60 * 60)

#         response = Response({"status": "success", "message": f"All featured products.", "data": product_data}, status=status.HTTP_200_OK)
#         response['X-Cache-Source'] = source
#         return response
    

#     @handle_exceptions
#     def top_deals_products(self, request, *args, **kwargs):
#         cache_key = 'top_deals_products'
#         product_data = cache.get(cache_key)
#         source = "cache" if product_data else "database"

#         if not product_data:
#             queryset = Product.objects.filter(top_deal=True).order_by("-date_created")
#             serializer = self.serializer_class(queryset, many=True)

#             product_data = []
#             for product in serializer.data:
#                 product_ins = Product.objects.get(id=product['id'])
#                 average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#                 rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#                 selected_fields = {
#                     'id': product.get('id'),
#                     'name': product.get('name'),
#                     'price': product.get('price'),
#                     'discount': product.get('discount'),
#                     'reviews': rounded_average_rating,
#                     'images': product.get('images')                     
#                 }
#                 product_data.append(selected_fields)

#             cache.set(cache_key, product_data, 60 * 60)
        
#         response =  Response({"status": "success", "message": "All top deals products.", "data": product_data}, status=status.HTTP_200_OK)
#         response['X-Cache-Source'] = source
#         return response
    
#     @handle_exceptions
#     def top_week_products(self, request, *args, **kwargs):
#         cache_key = 'top_week_products'
#         product_data = cache.get(cache_key)
#         source = "cache" if product_data else "database"
#         seven_days_ago = timezone.now() - timedelta(days=7)
#         # queryset = Product.objects.filter(date_created__gte=seven_days_ago).order_by("-date_created").order_by("?")

#         if not product_data:
#             queryset = Product.objects.all().order_by("?")[:8]
#             serializer = self.serializer_class(queryset, many=True)
#             product_data = []
#             for product in serializer.data:
#                 product_ins = Product.objects.get(id=product['id'])
#                 average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#                 rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#                 selected_fields = {
#                     'id': product.get('id'),
#                     'name': product.get('name'),
#                     'price': product.get('price'),
#                     'discount': product.get('discount'),
#                     'reviews': rounded_average_rating,
#                     'images': product.get('images')                     
#                 }
#                 product_data.append(selected_fields)

#             cache.set(cache_key, product_data, 60 * 60)
#         response = Response({"status": "success", "message": "All top week's products.", "data": product_data}, status=status.HTTP_200_OK)
#         response['X-Cache-Source'] = source
#         return response
    
#     @handle_exceptions
#     def view_product(self, request, product_id, *args, **kwargs):
#         cache_key = f'view_product_{product_id}'
#         product = cache.get(cache_key)

#         if not product:
#             product = Product.objects.filter(id=product_id).first()

#             if not product:
#                 return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
                               
#             cache.set(cache_key, product, 60 * 60)
            
#         serializer = self.serializer_class(product) 
#         return Response({"status": "success", "message": f"{product.name} Product details.", "data": serializer.data}, status=status.HTTP_200_OK)

#     @handle_exceptions
#     def filter_by_category(self, request, category_id, *args, **kwargs):
#         products = Product.objects.filter(category=category_id).order_by("-date_created")
#         category_name = Category.objects.filter(id=category_id).first()

#         if not category_name:
#             return Response({"status": "failed", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             serializer = self.serializer_class(products, many=True)
            
#             products_data = []
#             for product in serializer.data:
#                 product_ins = Product.objects.get(id=product['id'])
#                 average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#                 rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#                 selected_fields = {
#                     'id': product.get('id'),
#                     'name': product.get('name'),
#                     'price': product.get('price'),
#                     'discount': product.get('discount'),
#                     'reviews': rounded_average_rating,
#                     'images': product.get('images'),                      
#                 }
#                 products_data.append(selected_fields)
#             return Response({"status": "success", "message": f"{category_name.category} category products.", "data": products_data}, status=status.HTTP_200_OK)
        
    
#     @handle_exceptions
#     def filter_by_subcategory(self, request, subcategory_id, *args, **kwargs):
#         products = Product.objects.filter(subcategory=subcategory_id).order_by("-date_created")
#         subcategory_name = Subcategory.objects.filter(id=subcategory_id).first()

#         if not subcategory_name:
#             return Response({"status": "failed", "message": "Subcategory not found."}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             serializer = self.serializer_class(products, many=True)

#             products_data = []
#             for product in serializer.data:
#                 product_ins = Product.objects.get(id=product['id'])
#                 average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#                 rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#                 selected_fields = {
#                     'id': product.get('id'),
#                     'name': product.get('name'),
#                     'price': product.get('price'),
#                     'discount': product.get('discount'),
#                     'reviews': rounded_average_rating,
#                     'images': product.get('images'),                     
#                 }
#                 products_data.append(selected_fields)
#             return Response({"status": "success", "message": f"{subcategory_name.subcategory} subcategory products.", "data": products_data}, status=status.HTTP_200_OK)


#     @handle_exceptions
#     @action(detail=False, methods=['post'])
#     def filter_by_price_range(self, request):
#         product_query = Product.objects.filter().order_by("-date_created")
#         category = request.query_params.get('category', None)
#         subcategory = request.query_params.get('subcategory', None)
#         min_price = request.query_params.get('min_price', None)
#         max_price = request.query_params.get('max_price', None)
        
#         if min_price is None or max_price is None:
#             return Response({"status": "failed", "message": "field cannot be none."}, status=status.HTTP_400_BAD_REQUEST)
#         elif min_price is not None and max_price is not None:
#             if float(min_price) > float(max_price):
#                 return Response({"status": "failed", "message": "min_price cannot be greater than max_price"}, status=status.HTTP_400_BAD_REQUEST)
        
#         if category is not None:
#             if not Category.objects.filter(id=category).first():
#                 return Response({"status": "failed", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(category=category)
#                 name = Category.objects.filter(id=category).first()

#         if subcategory is not None:
#             if not Subcategory.objects.filter(id=subcategory).first():
#                 return Response({"status": "failed", "message": "Subcategory not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(subcategory=subcategory)
#                 name = Subcategory.objects.filter(id=subcategory).first()

#         if min_price is not None:
#             queryset = queryset.filter(price__gte=min_price)
#         if max_price is not None:
#             queryset = queryset.filter(price__lte=max_price)

#         serializer = self.serializer_class(queryset, many=True)
#         products_data = []
#         for product in serializer.data:
#             product_ins = Product.objects.get(id=product['id'])
#             average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#             rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#             selected_fields = {
#                 'id': product.get('id'),
#                 'name': product.get('name'),
#                 'price': product.get('price'),
#                 'discount': product.get('discount'),
#                 'reviews': rounded_average_rating,
#                 'images': product.get('images'),                     
#             }
#             products_data.append(selected_fields)
#         return Response({"status": "success", "message": f"{name} products between ₦{min_price} and ₦{max_price}.", "data": products_data}, status=status.HTTP_200_OK)
    

#     @handle_exceptions
#     def filter_price_under(self, request):
#         product_query = Product.objects.all().order_by("-date_created")
#         category = request.query_params.get('category', None)
#         subcategory = request.query_params.get('subcategory', None)
#         price_under = request.query_params.get('price_under', None)

#         if category is not None:
#             if not Category.objects.filter(id=category).first():
#                 return Response({"status": "failed", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(category=category)
#                 name = Category.objects.filter(id=category).first()

#         if subcategory is not None:
#             if not Subcategory.objects.filter(id=subcategory).first():
#                 return Response({"status": "failed", "message": "Subcategory not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(subcategory=subcategory)
#                 name = Subcategory.objects.filter(id=subcategory).first()

#         if price_under is None:
#             return Response({"status": "failed", "message": "field cannot be none."}, status=status.HTTP_400_BAD_REQUEST)
#         elif price_under is not None:
#             queryset = queryset.filter(price__lt=price_under)
            
#         serializer = self.serializer_class(queryset, many=True)

#         products_data = []
#         for product in serializer.data:
#             product_ins = Product.objects.get(id=product['id'])
#             average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#             rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#             selected_fields = {
#                 'id': product.get('id'),
#                 'name': product.get('name'),
#                 'price': product.get('price'),
#                 'discount': product.get('discount'),
#                 'reviews': rounded_average_rating,
#                 'images': product.get('images'),                     
#             }
#             products_data.append(selected_fields)
#         return Response({"status": "success", "message": f"{name} products under ₦{price_under}", "data": products_data}, status=status.HTTP_200_OK)
    

#     @handle_exceptions
#     @action(detail=False, methods=['post'])
#     def filter_from_price_above(self, request):
#         product_query = Product.objects.all().order_by("-date_created")
#         category = request.query_params.get('category', None)
#         subcategory = request.query_params.get('subcategory', None)
#         filter_from_price_above = request.query_params.get('filter_from_price_above', None)
        
#         if filter_from_price_above is None:
#             return Response({"status": "failed", "message": "field cannot be none"}, status=status.HTTP_400_BAD_REQUEST)
#         if category is not None:
#             if not Category.objects.filter(id=category).first():
#                 return Response({"status": "failed", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(category=category)
#                 name = Category.objects.filter(id=category).first()
#         if subcategory is not None:
#             if not Subcategory.objects.filter(id=subcategory).first():
#                 return Response({"status": "failed", "message": "Subcategory not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(subcategory=subcategory)
#                 name = Subcategory.objects.filter(id=subcategory).first()
        
#         elif filter_from_price_above is not None:
#             queryset = queryset.filter(price__gte=filter_from_price_above)
        
#         serializer = self.serializer_class(queryset, many=True)
#         products_data = []
#         for product in serializer.data:
#             product_ins = Product.objects.get(id=product['id'])
#             average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#             rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#             selected_fields = {
#                 'id': product.get('id'),
#                 'name': product.get('name'),
#                 'price': product.get('price'),
#                 'discount': product.get('discount'),
#                 'reviews': rounded_average_rating,
#                 'images': product.get('images'),                     
#             }
#             products_data.append(selected_fields)
#         return Response({"status": "success", "message": f"{name} products from ₦{filter_from_price_above} and above", "data": products_data}, status=status.HTTP_200_OK)
    

#     @handle_exceptions
#     def filter_by_ratings(self, request):
#         rating = request.query_params.get('rating', None)
#         # product_query = Product.objects.annotate(average_rating=Avg('reviews__rating')).filter(average_rating=rating).order_by("-date_created")
#         product_query = Product.objects.annotate(average_rating=Avg('reviews__rating'))
#         category = request.query_params.get('category', None)
#         subcategory = request.query_params.get('subcategory', None)
        
#         if rating is None:
#             return Response({"status": "failed", "message": "Rating parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
#         if category is not None:
#             if not Category.objects.filter(id=category).first():
#                 return Response({"status": "failed", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(category=category)
#                 name = Category.objects.filter(id=category).first()
#         if subcategory is not None:
#             if not Subcategory.objects.filter(id=subcategory).first():
#                 return Response({"status": "failed", "message": "Subcategory not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(subcategory=subcategory)
#                 name = Subcategory.objects.filter(id=subcategory).first() 
#         try:
#             rating = int(rating)
#         except ValueError:
#             return Response({"status": "failed", "message": "Rating must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        
#         filtered_products = []
#         for product in queryset:
#             if product.average_rating is not None:
#                 rounded_average_rating = math.ceil(product.average_rating)
#                 if rounded_average_rating == rating:
#                     filtered_products.append(product)
        
#         serializer = self.serializer_class(filtered_products, many=True)
#         products_data = []
        
#         for product in serializer.data:
#             product_ins = Product.objects.get(id=product['id'])
#             average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#             rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#             selected_fields = {
#                 'id': product.get('id'),
#                 'name': product.get('name'),
#                 'price': product.get('price'),
#                 'discount': product.get('discount'),
#                 'reviews': rounded_average_rating,
#                 'images': product.get('images'),                     
#             }
#             products_data.append(selected_fields)
#         return Response({"status": "success", "message": f"{name} products with {rating} stars", "data": products_data}, status=status.HTTP_200_OK)
    

#     @handle_exceptions
#     def filter_by_name(self, request):
#         product_name = request.query_params.get('name', None)
#         product_query = Product.objects.filter(name__icontains=product_name).order_by("-date_created")
#         category = request.query_params.get('category', None)
#         subcategory = request.query_params.get('subcategory', None)
        
#         if product_name is None:
#             return Response({"status": "failed", "message": "Name parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
#         if category is not None:
#             if not Category.objects.filter(id=category).first():
#                 return Response({"status": "failed", "message": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(category=category)
#                 name = Category.objects.filter(id=category).first()
#         if subcategory is not None:
#             if not Subcategory.objects.filter(id=subcategory).first():
#                 return Response({"status": "failed", "message": "Subcategory not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 queryset = product_query.filter(subcategory=subcategory)
#                 name = Subcategory.objects.filter(id=subcategory).first()

#         serializer = self.serializer_class(queryset, many=True)
#         products_data = []
#         for product in serializer.data:
#             product_ins = Product.objects.get(id=product['id'])
#             average_rating = product_ins.reviews.aggregate(Avg('rating'))['rating__avg']
#             rounded_average_rating = math.ceil(average_rating) if average_rating is not None else 0

#             selected_fields = {
#                 'id': product.get('id'),
#                 'name': product.get('name'),
#                 'price': product.get('price'),
#                 'discount': product.get('discount'),
#                 'reviews': rounded_average_rating,
#                 'images': product.get('images'),                     
#             }
#             products_data.append(selected_fields)
#         return Response({"status": "success", "message": f"{name} products with name '{product_name}'.", "data": products_data}, status=status.HTTP_200_OK)

# class CartViewSets(viewsets.ViewSet): 
#     serializer_class = CartItemSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]

#     @handle_exceptions
#     def add_to_cart(self, request):
#         session_key = request.data.get("session_key")
#         product_id = request.data.get("product_id")
#         quantity = request.data.get('quantity', 1)  # default quantity is 1
#         product = Product.objects.filter(id=product_id).first()

#         if not product:
#             return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#         elif request.user.is_authenticated:
#             cart, _ = Cart.objects.get_or_create(user=request.user) # get or create cart for user

#             # if session_key:
#             #     anonymous_cart = Cart.objects.filter(session_key=session_key, user=None).first() # check for cart with a user using session_key
#             #     if anonymous_cart:
#             #         for item in anonymous_cart.items.all():
#             #             existing_user_item = cart.items.filter(product=item.product).first()
#             #             if existing_user_item:
#             #                 existing_user_item.quantity += item.quantity
#             #                 existing_user_item.save()
#             #             else:
#             #                 item.cart = cart
#             #                 item.save()
#             #         anonymous_cart.delete()

#             cart_item = cart.items.filter(product=product).first()
#             if cart_item:
#                 cart_item.quantity += int(quantity)
#                 cart_item.save()
#             else:
#                 cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price, discount=product.discount)

#             serializer = self.serializer_class(cart_item)
#             return Response({"status": "success", "message": f"{product.name} added to cart."}, status=status.HTTP_200_OK)
#             # return Response({"status": "success", "message": "Product added to cart.", "data": serializer.data}, status=status.HTTP_200_OK)

#         else:
#             cart, _ = Cart.objects.get_or_create(user=None, session_key=session_key)
#             cart_item = cart.items.filter(product=product).first()
#             if cart_item:
#                 cart_item.quantity += int(quantity)
#                 cart_item.save()
#             else:
#                 cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity, price=product.price, discount=product.discount)

#             serializer = self.serializer_class(cart_item)
#             return Response({"status": "success", "message": f"{product.name} added to cart."}, status=status.HTTP_200_OK)
#             # return Response({"status": "success", "message": "Product added to cart.", "data": serializer.data}, status=status.HTTP_200_OK)
    
#     @handle_exceptions
#     def cart(self, request, *args, **kwargs):

#         if request.user.is_authenticated:
#             carts = Cart.objects.filter(user=request.user)
#             serializer = CartSerializer(carts, many=True)
#             return Response({"status": "success", "message": "Your cart", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             # For anonymous users, create an anonymous cart and return it
#             # session_key = request.session.session_key
#             session_key = request.query_params.get('session_key')
#             if not session_key:
#                 return Response({"status": "failed", "message": "Provide session key"}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 cart_none = Cart.objects.filter(user=None, session_key=session_key)
#                 serializer = CartSerializer(cart_none, many=True)
#                 return Response({"status": "success", "message": "Anonymous user cart", "data": serializer.data})
        
#     @handle_exceptions
#     def increase_item_quantity(self, request):
#         session_key = request.data.get("session_key")
#         cart_item_id = request.data.get("cart_item_id")
#         quantity = request.data.get('quantity', 1)  # default quantity is 1

#         cart_item = CartItem.objects.filter(id=cart_item_id).first()
#         if not session_key:
#             return Response({"status": "failed", "message": "Provide session key"}, status=status.HTTP_400_BAD_REQUEST)
#         elif not cart_item:
#             return Response({"status": "failed", "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
#         # Check if the cart item belongs to the user's cart
#         elif (not request.user.is_authenticated and cart_item.cart.session_key != session_key) or (request.user.is_authenticated and cart_item.cart.user != request.user):
#             return Response({"status": "failed", "message": "This item does not belong to your cart"}, status=status.HTTP_403_FORBIDDEN)
#         else:
#             cart_item.quantity += int(quantity)
#             cart_item.save()

#             serializer = self.serializer_class(cart_item)
#             return Response({"status": "success", "message": f"{quantity} quantity increase for {cart_item.product}", "data": serializer.data}, status=status.HTTP_200_OK)
    
#     @handle_exceptions
#     def decrease_item_quantity(self, request):
#         session_key = request.data.get("session_key")
#         cart_item_id = request.data.get("cart_item_id")
#         quantity = request.data.get('quantity', 1)  # default quantity is 1

#         cart_item = CartItem.objects.filter(id=cart_item_id).first()
#         if not session_key:
#             return Response({"status": "failed", "message": "Provide session key"}, status=status.HTTP_400_BAD_REQUEST)
#         elif not cart_item:
#             return Response({"status": "failed", "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
#         elif (not request.user.is_authenticated and cart_item.cart.session_key != session_key) or (request.user.is_authenticated and cart_item.cart.user != request.user):
#             return Response({"status": "failed", "message": "This item does not belong to your cart"}, status=status.HTTP_403_FORBIDDEN)
#         else:
#             if cart_item.quantity <= int(quantity):
#                 return Response({"status": "failed", "message": "Quantity cannot be decreased further"}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 cart_item.quantity -= int(quantity)
#                 cart_item.save()

#             serializer = self.serializer_class(cart_item)
#             return Response({"status": "success", "message": f"{quantity} quantity decreased from {cart_item.product}", "data": serializer.data}, status=status.HTTP_200_OK)
    
#     @handle_exceptions
#     def remove_from_cart(self, request):
#         session_key = request.data.get("session_key")
#         cart_item_id = request.data.get("cart_item_id")
#         cart_item = CartItem.objects.filter(id=cart_item_id).first()

#         if not session_key:
#             return Response({"status": "failed", "message": "Provide session key"}, status=status.HTTP_400_BAD_REQUEST)
#         elif not cart_item:
#             return Response({"status": "failed", "message": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
#         elif (not request.user.is_authenticated and cart_item.cart.session_key != session_key) or (request.user.is_authenticated and cart_item.cart.user != request.user):
#             return Response({"status": "failed", "message": "This item does not belong to your cart"}, status=status.HTTP_403_FORBIDDEN)
#         else:
#             cart_item.delete()
#             return Response({"status": "success", "message": f"{cart_item.product} removed from cart"}, status=status.HTTP_204_NO_CONTENT)
        
#     @handle_exceptions
#     def merge_cart(self, request, *args, **kwargs):
#         user_cart = Cart.objects.filter(user=request.user).first() # Get the user's cart
#         session_key = request.data.get("session_key") # request.session.session_key # Get the session key from the request's session

#         if session_key:
#             anonymous_cart = Cart.objects.filter(user=None, session_key=session_key).first()  # Get the anonymous cart based on the session key
#             if anonymous_cart:
#                 # Merge items from the anonymous cart into the user's cart
#                 if user_cart:
#                     for item in anonymous_cart.items.all():
#                         product = item.product
#                         user_existing_item = user_cart.items.filter(product=product).first() # Check if the same product exists in the user's cart
#                         if user_existing_item:
#                             user_existing_item.quantity += item.quantity
#                             user_existing_item.save()
#                         else:
#                             CartItem.objects.create(cart=user_cart, product=product, quantity=item.quantity)

#                     # Delete the anonymous cart after merging
#                     anonymous_cart.delete()
#                 else:
#                     anonymous_cart.user = request.user
#                     anonymous_cart.session_key = None
#                     anonymous_cart.save()
               
#                 # CartItem.objects.create(cart=user_cart, product=product, quantity=item.quantity)

                

#         return Response({"status": "success", "message": "Cart merged successfully"}, status=status.HTTP_200_OK)

# class CheckOutAndOrderViewSet(viewsets.ViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Order.objects.all()

#     @handle_exceptions
#     def checkout(self, request):
#         cart = request.user.carts.first()
#         if not cart or not cart.items.exists():
#             return Response({"status": "failed", "message": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             current_date = datetime.now().date()  # Get the current date

#             # Calculate the delivery date based on the current date and estimated shipping time
#             shipping_time_days = 7  # Example shipping time in days
#             delivery_date = current_date + timedelta(days=shipping_time_days)  # convert to month and day format (e.g May 10)
#             delivery_date_str = delivery_date.strftime("%B %d")  # Format the delivery date as a string

#             # Construct the delivery date range string
#             delivery_date_range = delivery_date_str + " and " + (delivery_date + timedelta(days=7)).strftime("%B %d")
#             my_wallet = request.user.my_wallet.first() 
#             wallet_balance = my_wallet.balance
#             wallet_point = my_wallet.point
#             wallet_total = wallet_balance + wallet_point
#             cart = request.user.carts.first()
#             if cart:
#                 total_price = cart.total_price()  # Calculate the total price of items in the cart
#             else:
#                 total_price = Decimal('0')
#             delivery_fee = Decimal(2440)
#             service_charge = Decimal(200)
#             total = total_price + delivery_fee + service_charge
#             cart_item_count = cart.cart_items_count()
            
#             return Response({
#                 "status": "success",
#                 "data":
#                 {"Delivery Details": f"Delivery will be between {delivery_date_range}. You will be notified upon delivery",
#                 "Customer Address": f"{request.user.address}, {request.user.lga}, {request.user.lga}, {request.user.state}",
#                 "Order Summary": {
#                 "wallet_balance": "₦{:,.2f}".format(wallet_balance),
#                 # "wallet_point": "₦{:,.2f}".format(wallet_point),
#                 # "wallet_total": "₦{:,.2f}".format(wallet_total),
#                 "total_items": {f"({cart_item_count})", "₦{:,.2f}".format(total_price)},
#                 # "total_price": total_price,
#                 "delivery_fee": "₦{:,.2f}".format(delivery_fee),
#                 "service_charge": "₦{:,.2f}".format(service_charge),
#                 "total": total
#                 }
#                 }}, status=status.HTTP_200_OK)

#     @handle_exceptions
#     def create_order(self, request, user, cart):
#         total_price = cart.total_price()  # Calculate the total price of items in the cart
#         delivery_fee = Decimal(2440)
#         service_charge = Decimal(200)
#         total_cost = total_price + delivery_fee + service_charge

#         # Create the order
#         order = Order.objects.create(
#             user=user,
#             order_id=random.randint(100000000, 999999999),
#             items_price=total_price,
#             delivery_fee=delivery_fee,
#             service_charge=service_charge,
#             total_price=total_cost,
#             shipping_address=request.data['shipping_address'],
#             shipping_method=request.data['shipping_method'],
#             payment_method=request.data['payment_method'],
#         )
#         # Create OrderProduct instances for each item in the cart
#         for cart_item in cart.items.all():
#             OrderProduct.objects.create(
#                 order=order,
#                 order_iid=order.order_id,
#                 product=cart_item.product,
#                 quantity=cart_item.quantity,
#                 price=cart_item.discount if cart_item.discount > 0.00 else cart_item.price,
#                 cost_price=cart_item.price,
#                 discount_price=cart_item.discount
#             )
#         return order, total_cost, delivery_fee, service_charge
    
#     @handle_exceptions
#     def verify_wallet_pin(self, request):
#         wallet = request.user.my_wallet.first()
#         wallet_pin = request.data.get('wallet_pin')

#         if wallet.pin == None:
#             return Response({"status": "failed", "message": "You haven't create your wallet PIN, create it."}, status=status.HTTP_400_BAD_REQUEST)
#         elif not check_password(wallet_pin, wallet.pin):
#             return Response({"status": "failed", "message": f"Incorrect wallet PIN."}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response({"status": "success", "message": f"PIN verifed successfully."}, status=status.HTTP_200_OK)


#     @handle_exceptions
#     def order(self, request):
#         cart = request.user.carts.first()
#         payment_method = request.data['payment_method']

#         total_price = cart.total_price()
#         delivery_fee = Decimal(2440)
#         service_charge = Decimal(200)
#         total_cost = total_price + delivery_fee + service_charge
        
#         if not cart or not cart.items.exists():
#             return Response({"status": "failed", "message": "Your cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
#         elif payment_method == "Wallet":
#             wallet = request.user.my_wallet.first()
        
#             # if wall.balance + wall.point < total_cost:
#             if wallet.balance < total_cost:
#                 return Response({"status": "failed", "message": "Your wallet balance is insufficient for this order."}, status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 order, total_cost, delivery_fee, service_charge = self.create_order(request, request.user, cart) # call the create_order method
#                 order_products = []
#                 total = Decimal(0)
#                 for cart_item in cart.items.all():
#                     sub_total = cart_item.sub_total()  # Calculate the subtotal of the product
#                     # total += sub_total  # Add the subtotal to the total price
#                     price = cart_item.discount if cart_item.discount > 0.00 else cart_item.price
#                     order_products.append({
#                         'product': cart_item.product.id,
#                         'quantity': cart_item.quantity,
#                         'price': price,
#                         'sub_total': sub_total
#                     })

#                     # Subtract the cart item quantity from the product quantity and save the product
#                     product = cart_item.product
#                     product.quantity -= cart_item.quantity
#                     product.save()

#                 # Clear the user's cart after placing the order
#                 cart.items.all().delete()
#                 wallet.balance -= int(total_cost)
#                 wallet.save()

#                 order.payment_status = "Success"
#                 order.save()
#                 unique_reference = f"pay_{request.user.first_name}_{total_cost}_{uuid.uuid4().hex[:10]}"
#                 order.reference = unique_reference
#                 order.save()
#                 Notification.objects.create(user=request.user, title="Your order is on it's way", message=f"Product(s) purchased successfully. Thank you!")
#                 Transaction.objects.create(user=request.user, beneficiary="Ajiroba Tech Ltd.", type="Product", channel="Wallet", reference=unique_reference, description="Purchase Product", items_price=total_price, amount=total_cost, status="Successful")
#                 # total_amount = sum(item['sub_total'] for item in order_products)
#                 reward_referral(request)
#                 product_order_email(request.user, order)
#                 return Response({"status": "success", "message": f"Order placed successfully. Order Code: {order.order_id}"}, status=status.HTTP_201_CREATED)
            
#         elif payment_method == "Electronic":
#             update_response = self.update_product_quantities(cart)
#             if update_response["status"] == "failed":
#                 return Response(update_response, status=status.HTTP_400_BAD_REQUEST)
            
#             payment_service = PaymentViewSet()
#             order, total_cost, delivery_fee, service_charge = self.create_order(request, request.user, cart) # call the create_order method
#             purchase_payment_response = payment_service.purchase_payment(request)
#             reference = purchase_payment_response.data.get('reference')
#             order.reference = reference
#             order.save()
#             update_trans = request.user.my_transactions.first()
#             update_trans.items_price = total_price
#             update_trans.save()
#             cart.items.all().delete()
#             return purchase_payment_response
#         else:
#             return Response({"status": "failed", "message": f"Payment failed: (select 'Wallet' or 'Electronic' as payment method)"}, status=status.HTTP_400_BAD_REQUEST)

#     @handle_exceptions
#     def verify_product_payment(self, request, reference):
#         verify_payment = PaymentViewSet()
#         verify_response = verify_payment.verify_purchase_payment(request, reference)

#         if verify_response.status_code == status.HTTP_400_BAD_REQUEST:
#             return verify_response
#         elif verify_response.status_code == status.HTTP_409_CONFLICT:
#             return verify_response
#         else:
#             update_order_status = Order.objects.filter(reference=reference, payment_status="Pending").first()
#             update_order_status.payment_status = "Success"
#             update_order_status.save()
#             reward_referral(request)
#             product_order_email(request.user, update_order_status)
#             Notification.objects.create(user=request.user, title="Your order is on it's way", message=f"Product(s) purchased successfully. Thank you!")
#             return Response({"status": "success", "message": "Payment verified"}, status=status.HTTP_200_OK)
    

#     @handle_exceptions
#     def update_product_quantities(self, cart):
#         for cart_item in cart.items.all():
#             product = cart_item.product
#             new_quantity = product.quantity - cart_item.quantity
#             if new_quantity < 0:
#                 return {"status": "failed", "message": f"Insufficient stock for product {product.name}."}
#             product.quantity = new_quantity
#             product.save()
#         return {"status": "success"}

# class ReviewViewSet(viewsets.ModelViewSet):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     @handle_exceptions
#     def query(self, product_id):
#         try:
#             return Product.objects.get(pk=product_id)
#         except Product.DoesNotExist:
#             return None

#     @handle_exceptions
#     def create_product_review(self, request, *args, **kwargs):
#         user = request.user
#         product_id = request.data.get('product_id')
#         product = self.query(product_id)
        
#         if not product:
#             return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             serializer.save(user=user, product=product)
#             return Response({"status": "success", "message": "Review created", "data": serializer.data}, status=status.HTTP_201_CREATED)
#         except IntegrityError:
#             return Response({"status": "failed", "message": "You have already reviewed this product."}, status=status.HTTP_409_CONFLICT)

#     @handle_exceptions
#     def update_product_review(self, request, *args, **kwargs):
#         user = request.user
#         product_id = request.data.get('product_id')
#         product = self.query(product_id)
        
#         if not product:
#             return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
#         try:
#             review = Review.objects.get(user=user, product=product)
#         except Review.DoesNotExist:
#             return Response({"status": "failed", "message": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = self.get_serializer(review, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(user=user, product=product, date_modify=timezone.now())
#         return Response({"status": "success", "message": "Product Review updated", "data": serializer.data}, status=status.HTTP_201_CREATED)




# # 































































# return Response(
    #     {"status": "success",
    #     "message": "Order placed successfully.",
    #     "order_id": order.id,
    #     "order_products": order_products,
    #     "delivery_fee": delivery_fee,
    #     "service_charge": service_charge,
    #     "total_amount": total_cost},
    #     status=status.HTTP_201_CREATED)

# #####

# serializer = CheckoutSerializer({
#             "wallet_balance": wallet,
#             "total_item": cart_item_count,
#             "total_price": total_price,
#             "delivery_fee": delivery_fee,
#             "service_charge": service_charge,
#             "total": total
#         })




















































































# class AddToCartViewSet(viewsets.ViewSet): 
#     serializer_class = CartItemSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [AllowAny]

#     @handle_exceptions
#     def create(self, request, id):
#         session_key = request.data["session_key"]
#         quantity = request.data.get('quantity', 1)  # default quantity is 1
#         product = Product.objects.filter(id=id).first()

#         if not product:
#             return Response({"status": "failed", "message": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
#         elif request.user.is_authenticated: # Check if the user has an active cart, create one if not
#             cart, created = Cart.objects.get_or_create(user=request.user)

#             cart_item = CartItem.objects.filter(cart=cart, product=product).first() # Try to get the cart item without the quantity field
#             if cart_item: # If the item already exists in the cart, update the quantity
#                 cart_item.quantity += int(quantity) 
#                 cart_item.save()
#             else:
#                 # If the item does not exist, create a new one
#                 cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

#             serializer = self.serializer_class(cart_item)
#             return Response({"status": "success", "message": "Product added to cart.", "data": serializer.data}, status=status.HTTP_200_OK)
#         else:
#             # Simulate an anonymous user by not providing a session key
#             cart, created = Cart.objects.get_or_create(user=None, session_key=session_key)

#             # Try to get the cart item without the quantity field
#             cart_item = CartItem.objects.filter(cart=cart, product=product).first()
#             if cart_item:
#                 # If the item already exists in the cart, update the quantity
#                 cart_item.quantity += int(quantity)
#                 cart_item.save()
#             else:
#                 # If the item does not exist, create a new one
#                 cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

#             serializer = self.serializer_class(cart_item)
#             return Response({"status": "success", "message": "Product added to cart.", "data": serializer.data}, status=status.HTTP_200_OK)




# class AddToCartViewSet(viewsets.ViewSet): 
#     serializer_class = CartItemSerializer
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def create(self, request, id):
#         product_id = request.data.get('product_id')
#         quantity = request.data.get('quantity', 1)  # default quantity is 1

#         product = Product.objects.filter(id=id).first()
#         if not product:
#             return Response({"status": "failed", "message": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

#         # Check if the user has an active cart, create one if not
#         cart, created = Cart.objects.get_or_create(user=request.user)

#         # Add the product to the cart
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#         if not created:
#             # If the item already exists in the cart, update the quantity
#             cart_item.quantity += int(quantity)
#             cart_item.save()

#         serializer = self.serializer_class(cart_item)
#         return Response({"status": "success", "message": "product added to cart", "data": serializer.data}, status=status.HTTP_200_OK)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response({
#             "status": "success",
#             "message": "Product details",
#             "data": serializer.data
#         })





