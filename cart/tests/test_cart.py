import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_create_cart_success(client, login_user, create_book):
    data = {
        "book": 7,
        "total_quantity": 2
    }
    url = reverse("cart")
    response = client.post(url, data, **login_user)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_cart_failure(client, login_user, create_book):
    data = {
        "book": 5,
        "total_quantity": 2
    }
    url = reverse("cart")
    response = client.post(url, data, **login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_cart_success(client, login_user, create_cart):
    url = reverse("cart")
    response = client.get(url, **login_user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_cart_failure(client, login_user, create_cart):
    url = reverse("cart")
    response = client.get(url, login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_cart_success(client, login_user, create_cart):
    data = {
        "id": 2
    }
    url = reverse("cart")
    response = client.delete(url, data, **login_user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_cart_failure(client, login_user, create_cart):
    data = {
        "id": 10
    }
    url = reverse("cart")
    response = client.delete(url, data, **login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_isordered_success(client, login_user, create_cart):
    data = {
        "id": 1
    }
    url = reverse("order")
    response = client.post(url, data, **login_user)
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_isordered_failure(client, login_user, create_cart):
    data = {
        "id": 10
    }
    url = reverse("order")
    response = client.post(url, data, **login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_get_isordered_success(client, login_user, create_isordered):
    url = reverse("order")
    response = client.get(url, **login_user)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_isordered_failure(client, login_user, create_isordered):
    url = reverse("order")
    response = client.get(url, login_user)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_isordered_success(client, login_user, create_isordered):
    data = {
        "id": 1
    }
    url = reverse("order")
    response = client.delete(url, data, **login_user)
    assert response.status_code == 200


@pytest.mark.abc
@pytest.mark.django_db
def test_delete_isordered_failure(client, login_user, create_isordered):
    data = {
        "id": 5
    }
    url = reverse("order")
    response = client.delete(url, data, **login_user)
    assert response.status_code == 400
