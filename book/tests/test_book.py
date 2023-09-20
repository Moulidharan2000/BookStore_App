from rest_framework.reverse import reverse
import pytest


def test_create_book_success(client, login_user):
    data = {
        "name": "gfgh",
        "author": "gatftfg",
        "description": "jhjy",
        "price": 1000
    }
    url = reverse("books")
    response = client.post(url, data, **login_user)
    print(response.data)
    assert response.status_code == 201


def test_create_book_failure(client, login_user):
    data = {
        "name": "sdgs",
        "author": "hj1566",
        "description": "jhjy",
        "price": 1000
    }
    url = reverse("books")
    response = client.post(url, data, **login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_book_success(client, login_user, create_book):
    url = reverse("books")
    response = client.get(url, **login_user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_book_failure(client, login_user):
    url = reverse("books")
    response = client.get(url, login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_book_success(client, login_user, create_book):
    data = {
        "id": 3,
        "name": "jksahf",
        "author": "aklfj",
        "description": "hjabf",
        "price": 1250
    }
    url = reverse("books")
    response = client.put(url, data, **login_user)
    assert response.status_code == 200
    assert response.data["data"]["name"] == "jksahf"


@pytest.mark.django_db
def test_update_book_failure(client, login_user, create_book):
    data = {
        "id": 2,
        "name": "jksahf",
        "author": 14564,
        "description": "hjabf",
        "price": 1250
    }
    url = reverse("books")
    response = client.put(url, data, **login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_book_success(client, login_user, create_book):
    data = {
        "id": 5,
    }
    url = reverse("books")
    response = client.delete(url, data, **login_user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_book_failure(client, login_user, create_book):
    data = {
        "id": 1,
    }
    url = reverse("books")
    response = client.delete(url, data, **login_user)
    assert response.status_code == 400


