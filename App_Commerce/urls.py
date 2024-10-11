from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Commerce.views import *
from knox import views as knox_views


urlpatterns = [
   path('create-category/', CategoryViewSets.as_view({"post": "create_category"}), name='category-create'),
   path('list-categories/', CategoryViewSets.as_view({"get": "list_categories"}), name='categories-list'),
   path('create-subcategory/', CategoryViewSets.as_view({"post": "create_subcategory"}), name='sucategory-create'),
   path('list-subcategories/', CategoryViewSets.as_view({"get": "list_subcategories"}), name='subcategories-list'),
  
]