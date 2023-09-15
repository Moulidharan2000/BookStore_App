import os
import re

import jwt
from django.contrib.auth.hashers import make_password
from rest_framework.reverse import reverse
from django.core.mail import send_mail
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import JWToken, user_verify
from drf_yasg.utils import swagger_auto_schema


class UserRegister(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer, operation_summary="User Register")
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            superuser = request.data.get("superuser")
            serializer.save()
            key = os.environ.get("SUPERUSER")
            user = User.objects.get(username=request.data.get("username"))
            if superuser == key:
                user.is_superuser = True
                user.save()
            token = JWToken.encode({"user": serializer.data.get("id"), "aud": "register"})
            subject = 'User Registered'
            message = f'{request.get_host()}/{reverse("verify_user")}?token={token}'
            from_email = os.environ.get("EMAIL_HOST_USER")
            recipient_list = [request.data.get("email")]
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "Email Sent and User Registered", "status": 201, "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    @swagger_auto_schema(request_body=LoginSerializer, operation_summary="Login User")
    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            token = JWToken.encode({"user": serializer.data.get("id"), "aud": "login"})
            return Response({"message": "User Login Success", "status": 200, "Token": token},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)


class VerifyUser(APIView):
    def post(self, request):
        try:
            query_param = request.GET.get("token")
            if not query_param:
                raise Exception("Invalid Token")
            token = jwt.decode(query_param, os.environ.get("key"), [os.environ.get("algorithm")], audience="register")
            user_id = token.get("user")
            user = User.objects.get(id=user_id)
            if user is None:
                raise Exception("User not Found")
            user.is_verified = True
            user.save()
            return Response({"message": "User Verification Success", "status": 200}, status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    def post(self, request):
        try:
            user = User.objects.get(username=request.data.get("username"))
            token = JWToken.encode({"user": user.username, "aud": "reset_password"})
            subject = 'Password Resetting'
            message = f'{request.get_host()}/{reverse("reset_pass")}?token={token}'
            from_email = os.environ.get("EMAIL_HOST_USER")
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
            return Response({"message": "Email Sent for Reset Password", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    def put(self, request):
        try:
            query_param = request.GET.get("token")
            if not query_param:
                raise Exception("Invalid Token")
            token = jwt.decode(query_param, os.environ.get("key"), [os.environ.get("algorithm")],
                               audience="reset_password")
            username = token.get("user")
            user = User.objects.get(username=username)
            new_password = request.data.get("new_password")
            password_pattern = "^[A-Za-z]{6}[0-9]{1}[!@#$&]{1}$"
            matcher = re.fullmatch(password_pattern, new_password)
            if not matcher:
                raise Exception("Invalid Password, Atleast 8 characters " +
                                "contains alphabets, 1 numerical character, 1 special character")
            confirm_password = request.data.get("confirm_password")
            if new_password != confirm_password:
                raise Exception("Password Should Match")
            user.password = make_password(request.data.get("confirm_password"))
            user.save()
            return Response({"message": "Password Reset Success", "status": 200},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)



