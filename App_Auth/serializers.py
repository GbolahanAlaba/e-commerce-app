from django.contrib.auth.models import User
from . models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import *
from . utils import *
from drf_extra_fields.fields import Base64ImageField



class AuthTokenSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField(
        label=_("Email/Phone"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email_or_phone = attrs.get('email_or_phone')
        password = attrs.get('password')

        if email_or_phone and password:
            # Check if email_or_phone is a valid email
            user = authenticate(request=self.context.get('request'), email=email_or_phone, password=password)
            if not user:
                # If not a valid email, check if it's a valid phone number
                user = authenticate(request=self.context.get('request'), phone=email_or_phone, password=password)

            if not user:
                raise NotAuthenticated({"status": "failed", "message": "Incorrect login details"}, code=status.HTTP_401_UNAUTHORIZED)

        else:
            msg = _('Must include "email_or_phone" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class SignupSerializer(serializers.ModelSerializer):
    referral = serializers.CharField(max_length=100, required=False, allow_blank=True)
    # profile_image = Base64ImageField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('user_id', 'first_name', 'last_name', 'email', 'phone', 'password', 'referral', 'address', 'state', 'city', 'lga', 'residential', 'gender', 'agree_terms')
        extra_kwargs = {'password': {'write_only': True}}  # Ensure password is write-only
    
    def create(self, validated_data):
        profile_image = validated_data.pop('profile_image', None)
        
        # Set and save password before creating the user instance
        referral_code = generate_referral_code()
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.referral_code = referral_code
        user.save()

        # Save profile image if provided
        if profile_image:
            user.profile_image = profile_image
            user.save()

        return user

    def get_profile_image_url(self, obj):
        if obj.profile_image:
            return self.context['request'].build_absolute_uri(obj.profile_image.url)
        return None

