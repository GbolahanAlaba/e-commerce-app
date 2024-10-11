from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Commerce.views import *
from knox import views as knox_views


router = DefaultRouter()
# router.register(r'list_products', ProductsViewSet, basename='products')
# router.register(r'cart', CartViewSet, basename='cart')
router.register(r'check_outt', CheckOutAndOrderViewSet, basename='check_out')


urlpatterns = [
   # HOMEPAGE
   path('products/', ProductsViewSet.as_view({"get": "all_products"}), name='products'), # view_product
   path('featured_products/', ProductsViewSet.as_view({"get": "featured_products"}), name='featured_products'), # featured_products
   path('top_deals_products/', ProductsViewSet.as_view({"get": "top_deals_products"}), name='top_deals_products'), # top_deals_products
   path('top_week_products/', ProductsViewSet.as_view({"get": "top_week_products"}), name='top_week_products'), # top_week_products
   path('view_product/<str:product_id>/', ProductsViewSet.as_view({"get": "view_product"}), name='view_product'), # view_product

   # FILTERS
   path('filter_by_category/<str:category_id>/', ProductsViewSet.as_view({"get": "filter_by_category"}), name='filter_by_category'), # filter_by_category
   path('filter_by_subcategory/<str:subcategory_id>/', ProductsViewSet.as_view({"get": "filter_by_subcategory"}), name='filter_by_subcategory'), # filter_by_subcategory
   path('filter_by_price_range/', ProductsViewSet.as_view({"get": "filter_by_price_range"}), name='filter_by_price_range'), # filter_by_price_range
   path('filter_price_under/', ProductsViewSet.as_view({"get": "filter_price_under"}), name='filter_price_under'), # filter_price_under
   path('filter_from_price_above/', ProductsViewSet.as_view({"get": "filter_from_price_above"}), name='filter_from_price_above'), # filter_from_price_above
   path('filter_by_ratings/', ProductsViewSet.as_view({"get": "filter_by_ratings"}), name='filter_by_ratings'), # filter_by_ratings
   path('filter_by_name/', ProductsViewSet.as_view({"get": "filter_by_name"}), name='filter_by_name'), # filter_by_name

   # CART 
   path('add_to_cart/', CartViewSets.as_view({"post": "add_to_cart"}), name='add_to_cart'), # add to cart
   path('cart/', CartViewSets.as_view({"get": "cart"}), name='cart'), # cart
   path('increase_item_quantity/', CartViewSets.as_view({"put": "increase_item_quantity"}), name='increase_item_quantity'), # increase item quantity
   path('decrease_item_quantity/', CartViewSets.as_view({"put": "decrease_item_quantity"}), name='decrease_item_quantity'), # decrease item quantity
   path('remove_from_cart/', CartViewSets.as_view({"delete": "remove_from_cart"}), name='remove_from_cart'), # remove from cart
   path('merge_cart/', CartViewSets.as_view({"post": "merge_cart"}), name='merge_cart'), # merge_cart

   # ORDER
   path('checkout/', CheckOutAndOrderViewSet.as_view({"get": "checkout"}), name='checkout'), # checkout
   path('verify_wallet_pin/', CheckOutAndOrderViewSet.as_view({"post": "verify_wallet_pin"}), name='verify_wallet_pin'), # verify wallet pin
   path('order/', CheckOutAndOrderViewSet.as_view({"post": "order"}), name='order'), # order
   path('verify_product_payment/<str:reference>/', CheckOutAndOrderViewSet.as_view({'get': 'verify_product_payment'}), name='verify_product_payment'),

   #  REVIEWS
   path('create_product_review/', ReviewViewSet.as_view({"post": "create_product_review"}), name='create_product_review'),
   path('update_product_review/', ReviewViewSet.as_view({"put": "update_product_review"}), name='update_product_review'),
   

   # CATEGORY & SUBCATEGORY
   path('categories/', CategoryViewSets.as_view({"get": "list_categories"}), name='categories'), # categories
   path('categories_and_subcategories/', CategoryViewSets.as_view({"get": "categories_and_subcategories"}), name='categories_and_subcategories'), # category_subcategories
   path('category_and_subcategories/<str:category_id>/', CategoryViewSets.as_view({"get": "category_and_subcategories"}), name='category_and_subcategories'), # category_subcategories
   path('subcategories/', SubCategoryViewSets.as_view({"get": "list_subcategories"}), name='subcategories'), # subcategories

   path('delete_cache/', CategoryViewSets.as_view({"delete": "delete_cache"}), name='delete_cache'), # delete_cache
   path('', include(router.urls)),
  
]