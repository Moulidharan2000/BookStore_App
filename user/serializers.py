import re

from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email', 'phone', 'location']

    def validate(self, attrs):
        firstname = attrs.get("first_name")
        firstname_pattern = "^[A-Za-z]{3,8}$"
        matcher = re.fullmatch(firstname_pattern, firstname)
        if not matcher:
            raise Exception("Invalid Firstname, Atleast 8 characters")
        lastname = attrs.get("last_name")
        lastname_pattern = "^[A-Za-z]{3,8}"
        matcher = re.fullmatch(lastname_pattern, lastname)
        if not matcher:
            raise Exception("Invalid Lastname, Atleast 8 characters")
        username = attrs.get("username")
        username_pattern = "^[A-Za-z0-9]{3,8}$"
        matcher = re.fullmatch(username_pattern, username)
        if not matcher:
            raise Exception("Invalid Username, Atleast 8 characters")
        password = attrs.get("password")
        password_pattern = "^[A-Za-z]{6}[0-9]{1}[!@#$&]{1}$"
        matcher = re.fullmatch(password_pattern, password)
        if not matcher:
            raise Exception("Invalid Password, Atleast 8 characters " +
                            "contains alphabets, 1 numerical character, 1 special character")
        email = attrs.get("email")
        email_pattern = "^[a-z0-9]+?@{1}[a-z]{3,5}[.][a-z]{2,3}$"
        matcher = re.fullmatch(email_pattern, email)
        if not matcher:
            raise Exception("Invalid Email Address")
        phone = attrs.get("phone")
        phone_pattern = "^[6-9]{1}[0-9]{9}$"
        matcher = re.fullmatch(phone_pattern, str(phone))
        if not matcher:
            raise Exception("Invalid Phone Number")
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200, write_only=True)
    password = serializers.CharField(max_length=200, write_only=True)
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user = authenticate(**validated_data)
        if not user:
            raise Exception("Invalid Credentials")
        return user
