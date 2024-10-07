from django.db import models
from App_Auth.models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.utils import timezone



class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value

class UserManager(BaseUserManager):
    def create_user(self, email, phone, password=None):
        if not email:
            raise ValueError('user must have an email address')
        if not phone:
            raise ValueError('user must have an phone')
        
        user = self.model(
            email = self.normalize_email(email),
            phone = phone
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, phone, password):
        user = self.create_user(
            email = self.normalize_email(email),
            phone = phone,
            password = password,

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_approved = True
        user.save(using=self._db)

class User(AbstractBaseUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100, blank=True, null=True, default="")
    last_name = models.CharField(max_length=100, blank=True, null=True, default="")
    email = LowercaseEmailField(max_length=100, blank=True, null=True, default='', unique=True)
    phone = models.CharField(max_length=100, blank=True, null=True, default="", unique=True)
    password = models.CharField(max_length=100)
    referral = models.CharField(max_length=100, blank=True, null=True, default="")
    address = models.CharField(max_length=100, blank=True, null=True, default="")
    city = models.CharField(max_length=100, blank=True, null=True, default="")
    state = models.CharField(max_length=100, blank=True, null=True, default="")
    lga = models.CharField(max_length=100, blank=True, null=True, default="")
    residential = models.CharField(max_length=100, blank=True, null=True, default="")
    gender = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='users', default='', blank=True, null=True)
    referral_code = models.CharField(max_length=100, blank=True, null=True, default="")
    user_type = models.CharField(max_length=100, blank=True, null=True, default="")
    agree_terms = models.BooleanField(default=False)
    
    # required
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)   
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()

    def __str__(self):
        return str(self.first_name)
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class OTPModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=100, default='', null=True, unique=False)
    otp = models.IntegerField(default='', blank=True, null=True)
    count = models.IntegerField(default=1, help_text='Number of otp sent')
    expiry = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add = True, auto_now=False)

    class Meta:
        verbose_name = 'OTP Model'
        verbose_name_plural = 'OTPs'

    def __str__(self):
        return self.email