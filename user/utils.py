import os
import re
from datetime import datetime, timedelta
import jwt
from rest_framework import status
from rest_framework.response import Response
from user.models import User


class JWToken:
    @staticmethod
    def encode(payload):
        if 'exp' not in payload.keys():
            payload["exp"] = datetime.utcnow() + timedelta(hours=1)
        return jwt.encode(payload, key=os.environ.get("key"), algorithm=os.environ.get("algorithm"))

    @staticmethod
    def decode(token, aud):
        try:
            return jwt.decode(token, key=os.environ.get("key"), algorithms=[os.environ.get("algorithm")], audience=aud)
        except jwt.PyJWTError as e:
            raise e


def check_user(request):
    token = request.headers.get("token")
    if not token:
        raise Exception("Token Not Found")
    payload = JWToken.decode(token, aud="login")
    if "user" not in payload.keys():
        raise Exception("User Not Found")
    user = User.objects.filter(id=payload.get("user"))
    if not user.exists():
        raise Exception("User Not Found")
    return user.first()


def user_verify(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            user = check_user(request)
            request.data.update({"user": user.id})
            return function(self, request, *args, **kwargs)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)

    return wrapper


def super_user(function):
    def wrapper(self, request, *args, **kwargs):
        try:
            user = check_user(request)
            if not user.is_superuser:
                raise Exception("Not a SuperUser")
            request.data.update({"user": user.id})
            return function(self, request, *args, **kwargs)
        except Exception as ex:
            return Response({"message": str(ex), "status": 400, "data": {}},
                            status=status.HTTP_400_BAD_REQUEST)

    return wrapper


