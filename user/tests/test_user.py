from rest_framework.reverse import reverse
import pytest
from django.db.backends.base.creation import BaseDatabaseCreation


# class TestDatabase(BaseDatabaseCreation):
#     def _get_test_db_name(self):
#         print(self.connection.settings_dict)
#         return super()._get_test_db_name()

def test_register_user_success(client, django_user_model):
    data = {
        "first_name": "raj",
        "last_name": "rajesh",
        "username": "raju",
        "password": "password",
        "email": "rajirajesh10@gmail.com",
        "phone": 9865321470,
        "location": "Mumbai"
    }
    url = reverse("register")
    response = client.post(url, data, content_type="application/json")
    print(response.content)
    assert response.status_code == 201


def test_register_user_failure(client):
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


def test_login_user_success(client, register_user):
    data = {
        "username": "ramu",
        "password": "password"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 200


def test_login_user_failure(client, register_user):
    data = {
        "username": "ramu15648",
        "password": "password"
    }
    url = reverse("login")
    response = client.post(url, data, content_type="application/json")
    assert response.status_code == 400


def test_is_verified_success(client, register_user):
    url = reverse("verify_user")
    response = client.post(url, content_type="application/json")
    assert response.status_code == 200


def test_is_verified_failure(client, register_user):
    url = reverse("verify_user")
    response = client.post(url, content_type="application/json")
    assert response.status_code == 400


@pytest.mark.abc
def test_is_superuser_success(client, register_user, **login_user):
    data = {
        "id": 1
    }
    url = reverse("super_user")
    response = client.post(url, data, **login_user, content_type="application/json")
    assert response.status_code == 200


def test_is_superuser_failure(client, register_user, **login_user):
    data = {
        "id": 2
    }
    url = reverse("super_user")
    response = client.post(url, data, **login_user, content_type="application/json")
    assert response.status_code == 400
