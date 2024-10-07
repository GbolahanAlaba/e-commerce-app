from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from App_Auth.views import *
from knox import views as knox_views



router = DefaultRouter()
router.register(r'signin', AuthViewSets, basename='signin')
router.register(r'signup', AuthViewSets, basename='signup')

router.register(r'verify_account_activation', AuthViewSets, basename='verify_account_activation')
router.register(r'resend_account_activation_code', AuthViewSets, basename='resend_account_activation_code')

router.register(r'forgot_password', AuthViewSets, basename='forgot_password')
router.register(r'verify_reset_password_code', AuthViewSets, basename='verify_reset_password_code')

router.register(r'signout', LogoutViewSet, basename='signout')
router.register(r'signoutall', LogoutViewSet, basename='signoutall')


urlpatterns = [
   path('', include(router.urls)),  
   path('reset_password/<str:otp>/', AuthViewSets.as_view({"put": "put"}), name='verify_reset_password_code'), # reset password
   
  
]