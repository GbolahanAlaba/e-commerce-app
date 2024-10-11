from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Commerce.views import *
from knox import views as knox_views


urlpatterns = [
   path('create-category/', CategoryViewSets.as_view({"post": "create_category"}), name='category-create'),
   path('list-category/', CategoryViewSets.as_view({"post": "list_category"}), name='category-list'),
   path('create-subcategory/', CategoryViewSets.as_view({"post": "create_subcategory"}), name='sucategory-create'),
   path('list-category/', CategoryViewSets.as_view({"post": "list_category"}), name='subcategory-list'),
  
]