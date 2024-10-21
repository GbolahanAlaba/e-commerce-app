from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Auth.views import *
from knox import views as knox_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




router = DefaultRouter()
# router.register(r'signup', AuthViewSets, basename='signup')

router.register(r'verify_account_activation', AuthViewSets, basename='verify_account_activation')
router.register(r'resend_account_activation_code', AuthViewSets, basename='resend_account_activation_code')

router.register(r'forgot_password', AuthViewSets, basename='forgot_password')
router.register(r'verify_reset_password_code', AuthViewSets, basename='verify_reset_password_code')

router.register(r'signout', LogoutViewSet, basename='signout')
router.register(r'signoutall', LogoutViewSet, basename='signoutall')


urlpatterns = [
   path('', include(router.urls)), 
   path('signin/', AuthViewSets.as_view({"post": "signin"}), name='signin'),
   path('signup/', AuthViewSets.as_view({"post": "signup"}), name='signup'),
   path('reset_password/<str:otp>/', AuthViewSets.as_view({"put": "put"}), name='verify_reset_password_code'),

   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
   
]