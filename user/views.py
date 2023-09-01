import os
import jwt
from rest_framework.reverse import reverse
from django.core.mail import send_mail
from rest_framework.views import APIView
from .models import User
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from .utils import JWToken, user_verify
from drf_yasg.utils import swagger_auto_schema


# Create your views here.
class UserRegister(APIView):
    @swagger_auto_schema(request_body=RegisterSerializer, operation_summary="User Register")
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
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


class VerifySuperuser(APIView):
    @swagger_auto_schema(operation_summary="Verify_SuperUser")
    @user_verify
    def post(self, request):
        try:
            user = User.objects.get(id=request.data.get("user"))
            if not user:
                raise Exception("Invalid User")
            user.is_superuser = True if not user.is_superuser else False
            user.save()
            return Response({"message": "User Verification Success", "status": 200, "is_superuser": user.is_superuser},
                            status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}}, status=status.HTTP_400_BAD_REQUEST)


