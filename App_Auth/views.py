from django.http import JsonResponse
from django.shortcuts import render

from App import settings
from App_Auth.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import viewsets, permissions, status
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from knox.auth import AuthToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.signals import user_logged_in, user_logged_out
from . serializers import *
from django.db.models import Q
from . utils import *
from . tasks import *
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from datetime import date, datetime, timedelta
from django.utils import timezone



class AuthViewSets(viewsets.ModelViewSet):
    serializer_class = AuthTokenSerializer
    queryset = User.objects.all()

    @handle_exceptions
    def signin(self, request):
        email_or_phone = request.data['email_or_phone']

        # Check if email_or_phone exists as either email or phone number
        checkUser = User.objects.filter(Q(email=email_or_phone) | Q(phone=email_or_phone)).first()

        if checkUser is None:
            return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        elif not checkUser.is_active:
            return Response({"status": "failed", "message": "Account is not verified"}, status=status.HTTP_403_FORBIDDEN)

        else:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]
            user.last_login = timezone.now()
            user.save(update_fields=["last_login"])

            # Generate JWT Token (both access and refresh tokens)
            refresh = RefreshToken.for_user(user)  # This will create the JWT refresh and access tokens

            response_data = {
                "status": "success",
                "message": "Signin successfully",
                "data": {
                    # "user_id": user.user_id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": user.phone,
                    "address": user.address,
                    "state": user.state,
                    "lga": user.lga,
                    "residential": user.residential,
                    "gender": user.gender,
                    "referral_code": user.referral_code,
                    "is_staff": user.is_staff,
                },
                "tokens": {
                    "access": str(refresh.access_token),  # Return the access token
                    "refresh": str(refresh)  # Return the refresh token
                }
            }

            if user.profile_image:
                response_data['profile_image_url'] = request.build_absolute_uri(user.profile_image.url)

            return Response(response_data, status=status.HTTP_200_OK)

    @handle_exceptions
    def signup(self, request):
        email = request.data["email"]
        phone = request.data["phone"]
        referral = request.data.get('referral', '')

        if User.objects.filter(email=email):
            return Response({"status": "failed", "message": "Email already exist"}, status=status.HTTP_409_CONFLICT)
        elif not is_valid_email(email):
            return Response({"status": "failed", "message": "Invalid email address"}, status=status.HTTP_400_BAD_REQUEST)
        elif not is_valid_phone(phone):
            return Response({"status": "failed", "message": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)
        elif User.objects.filter(phone=phone):
             return Response({"status": "failed", "message": "Phone already exist"}, status=status.HTTP_409_CONFLICT)
        elif referral != "":
            if not User.objects.filter(referral_code=referral).exists():
                return Response({"status": "failed", "message": "Invalid referral code"}, status=status.HTTP_400_BAD_REQUEST)
    
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Wallet.objects.create(user=user)
        
        # _, token = AuthToken.objects.create(user)

        key = send_otp(email)
        OTPModel.objects.create(email=email, otp = key, expiry=timezone.now() + timedelta(minutes=5))
        send_activation_email(user, key)

        return Response({
            "status": "success",
            "message": "Signup successfully, OTP (%s) sent to your mail"%(key),
            "data": {
                "user_id": user.user_id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            },
            # "token": token
        }, status=status.HTTP_201_CREATED)

    @handle_exceptions
    def verify_account(self, request):
        otp = request.data['otp']
        
        chk = OTPModel.objects.filter(otp=otp).first() # checking if the generated otp is the same with the one in the otp row in the OTP model
        if not chk:
            return Response({"status": "failed", "message": "invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        elif chk.expiry < timezone.now():
            return Response({"status": "failed", "message": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(email=chk.email).first()
            user.is_active = True
            user.save()
            chk.delete()
            verified_account_email(user)
            return Response({"status": "success", "message": "Account activated successfully!"}, status=status.HTTP_200_OK)

    @handle_exceptions
    def resend_account_verificatio_otp(self, request):
        email = request.data['email']
        user = User.objects.filter(email=email).first() # checking if the staff ID exist in the user model

        if not user:
            return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        else:
            key = send_otp(email)
            if key:
                emailRecord = OTPModel.objects.filter(email=email).first() # checking if the email exist in the OTP table
                if emailRecord:
                    count = emailRecord.count
                    if count == 10:            
                        return Response({"status": "failed", "message": "OTP chances exceeded! Contact customer support"}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        emailRecord.count = count + 1
                        emailRecord.otp = key
                        emailRecord.date_created = timezone.now()
                        emailRecord.expiry = timezone.now() + timedelta(minutes=5)            
                        emailRecord.save()
                        send_activation_email(user, key)
                        return Response({"status": "success", "message": "OTP (%s) resent to your mail"%(key)}, status=status.HTTP_200_OK)
                else:        
                    OTPModel.objects.create(email=email, otp=key, expiry=timezone.now() + timedelta(minutes=5))
                    send_activation_email(user, key)
                    return Response({"status": "success", "message": "OTP (%s) resent to your mail"%(key)}, status=status.HTTP_200_OK)

    @handle_exceptions
    def forget_password(self, request):
        email = request.data['email']

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"status": "failed", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            key = send_otp(email)
            if key:
                emailRecord = OTPModel.objects.filter(email=email)
                if emailRecord.exists():
                    record = emailRecord.first()
                    count = record.count
                    if count == 10:
                        return Response({"status": "failed", "message": "OTP chances exceeded! Contact customer support"}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        record.count = count + 1
                        record.otp = key
                        record.date_created = timezone.now()
                        record.expiry = timezone.now() + timedelta(minutes=5)            
                        record.save()
                        forgot_password_email(user, key)
                        return Response({"status": "success", "message": "OTP (%s) sent to your mail"%(key)}, status=status.HTTP_200_OK)
                else:        
                    OTPModel.objects.create(email=email, otp=key, expiry=timezone.now() + timedelta(minutes=5))
                    forgot_password_email(user, key)
                    return Response({"status": "success", "message": "OTP (%s) sent to your mail"%(key)}, status=status.HTTP_200_OK)

    @handle_exceptions
    def reset_password(self, request, otp):
        password = request.data['password']
        check_otp = OTPModel.objects.filter(otp=otp).first()
        if not check_otp:
            return Response({"status": "failed", "message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        email = check_otp.email
            
        get_user = User.objects.filter(email=email).first()
        user = get_user
        user.set_password(password)
        user.save()

        expire_otp = OTPModel.objects.get(otp=otp)
        expire_otp.otp = 0
        expire_otp.save()

        return Response({"status": "success", "message":"You've reset your password successfully"}, status=status.HTTP_200_OK)

        
class LogoutViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @handle_exceptions
    def logout(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    @handle_exceptions
    def logout_all(self, request, format=None):
        request.user.auth_token_set.all().delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
  

    