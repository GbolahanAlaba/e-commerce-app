# Register your models here.
from django.contrib import admin
from . models import *
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'is_staff', 'is_active', 'last_login', 'created_at', 'modified_at']
    list_filter = ['first_name']
    search_fields = ['first_name']
    ordering = ['-created_at'] 

class OTPModelAdmin(admin.ModelAdmin):
    list_display = ['email', 'otp', 'count', 'created_at', 'expiry']
    list_filter = ['email']
    search_fields = ['email']
    ordering = ['-created_at'] 


admin.site.register(User, UserAdmin)
admin.site.register(OTPModel, OTPModelAdmin)

