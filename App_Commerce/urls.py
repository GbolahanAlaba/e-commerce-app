from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Commerce.views import *
from knox import views as knox_views


urlpatterns = [
   path('create-category/', CategoryViewSets.as_view({"post": "create_category"}), name='category-create'),
   path('list-categories/', CategoryViewSets.as_view({"get": "list_categories"}), name='categories-list'),
   path('create-subcategory/', CategoryViewSets.as_view({"post": "create_subcategory"}), name='subcategory-create'),
   path('list-subcategories/', CategoryViewSets.as_view({"get": "list_subcategories"}), name='subcategories-list'),

   # PRODUCTS
   path('create-product/', UploadProductViewSet.as_view({"post": "create_product"}), name='product-create'),
   path('update-product/<str:product_id>/', UploadProductViewSet.as_view({"put": "update_product"}), name='product-update'),
   path('all-products/', ProductsViewSet.as_view({"get": "all_products"}), name='products-all'),

   
   
  
]