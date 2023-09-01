import pytest
from rest_framework.reverse import reverse


@pytest.fixture()
def register_user(client):
    data = {
        "first_name": "haf",
        "last_name": "jhfjka",
        "username": "ramu",
        "password": "password",
        "email": "moulisitthan10@gmail.com",
        "phone": 234654897,
        "location": "jkfajk"
    }
    url = reverse("register")
    response = client.post(url, data, content_type="application/json")
    return response.data["data"]


@pytest.fixture
def user_verify(client):
    url = reverse("verify_user")
    response = client.post(url, content_type="application/json")
    return response.data["data"]


@pytest.fixture
def login_user(client):
    data = {
        "username": "ramu",
        "password": "password"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    return {"content_type": "application/json", "HTTP_TOKEN": response.data["token"]}


