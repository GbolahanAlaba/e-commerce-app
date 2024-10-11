from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Commerce.views import *
from knox import views as knox_views


urlpatterns = [
   # path('products/', ProductsViewSet.as_view({"get": "all_products"}), name='products'), # view_product
  
]