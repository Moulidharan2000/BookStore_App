import pytest
from rest_framework.reverse import reverse
from user.models import User


@pytest.fixture()
def register_user(client, django_user_model):
    data = {
        "first_name": "raj",
        "last_name": "rajesh",
        "username": "raju",
        "password": "passwo1$",
        "email": "rajirajesh10@gmail.com",
        "phone": "9865321470",
        "location": "Mumbai",
        "superuser": "admin"
    }
    url = reverse("register")
    response = client.post(url, data, content_type="application/json")
    user = User.objects.get(username="raju")
    if user:
        user.is_verified = True
    user.save()
    return response.data["data"]


@pytest.fixture
def login_user(client, register_user):
    data = {
        "username": "raju",
        "password": "passwo1$"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    return {"content_type": "application/json", "HTTP_TOKEN": response.data["Token"]}


@pytest.fixture
def create_book(client, login_user):
    data = {
        "name": "gfgh",
        "author": "gatftfg",
        "description": "jhjy",
        "price": 1000
    }
    url = reverse("books")
    response = client.post(url, data, **login_user)
    return response.data


@pytest.fixture
def create_cart(client, login_user, create_book):
    data = {
        "book": 7,
        "total_quantity": 2
    }
    url = reverse("cart")
    response = client.post(url, data, **login_user)
    return response.data


@pytest.fixture
def create_isordered(client, login_user, create_cart):
    data = {
        "id": 1
    }
    url = reverse("order")
    response = client.post(url, data, **login_user)
    return response.data
