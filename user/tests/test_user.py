from rest_framework.reverse import reverse
import pytest


def test_register_user_success(client, django_user_model):
    data = {
        "first_name": "raj",
        "last_name": "rajesh",
        "username": "raju",
        "password": "passwo1$",
        "email": "rajirajesh10@gmail.com",
        "phone": "9865321470",
        "location": "Mumbai"
    }
    url = reverse("register")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 201


def test_register_user_failure(client, django_user_model):
    data = {
        "first_name": "raj",
        "last_name": "rajesh",
        "username": "raju5646898",
        "password": "password231564",
        "email": "hsfkjfkjafka10@gmail.com",
        "phone": 9865321470,
        "location": "Mumbai"
    }
    url = reverse("register")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400


def test_login_user_success(client, register_user, django_user_model):
    data = {
        "username": "raju",
        "password": "passwo1$"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200


def test_login_user_failure(client, register_user, django_user_model):
    data = {
        "username": "ramu15648",
        "password": "password"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400

