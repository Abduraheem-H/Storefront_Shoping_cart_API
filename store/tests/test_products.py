from django.urls import reverse
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from pytest import mark
from model_bakery import baker
from store.models import Product


@pytest.fixture
def create_product():
    from model_bakery import baker
    from store.models import Product

    def _create_product(**kwargs):
        defaults = {
            "title": "Sample Product",
            "slug": "sample-product",
            "unit_price": 15.00,
            "inventory": 20,
            "description": "This is a sample product description.",
            "collection": baker.make("store.Collection"),
        }
        defaults.update(kwargs)
        return baker.make(Product, **defaults)

    return _create_product


@pytest.fixture
def product_payload(create_product):
    """Fixture for sample product data."""
    product = create_product()
    return {
        "title": product.title,
        "slug": product.slug,
        "unit_price": product.unit_price,
        "inventory": product.inventory,
        "description": product.description,
        "collection": product.collection.id,
    }


@pytest.fixture
def invalid_product_payload():
    """Fixture for invalid product data."""
    return {
        "title": "",
        "unit_price": "-10",
        "collection": "",
        "inventory": "-5",
    }


@mark.django_db
class TestCreateProduct:

    def test_if_user_is_anonymous_returns_401(
        self, api_client: APIClient, product_payload: dict
    ):
        response = api_client.post(reverse("store:product-list"), data=product_payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client: APIClient, product_payload: dict, authenticate
    ):
        authenticate(is_staff=False)
        response = api_client.post(reverse("store:product-list"), data=product_payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_201(
        self, api_client: APIClient, product_payload: dict, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.post(reverse("store:product-list"), data=product_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0

    def test_if_payload_is_invalid_returns_400(
        self, api_client: APIClient, invalid_product_payload: dict, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.post(
            reverse("store:product-list"), data=invalid_product_payload
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert "unit_price" in response.data
        assert "collection" in response.data
        assert "inventory" in response.data

    def test_if_payload_is_valid_returns_201(
        self, api_client: APIClient, product_payload: dict, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.post(reverse("store:product-list"), data=product_payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@mark.django_db
class TestRetrieveProduct:

    def test_if_product_exists_returns_200(self, api_client: APIClient, create_product):
        product = create_product()
        response = api_client.get(reverse("store:product-detail", args=[product.id]))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["id"] == product.id

    def test_if_product_does_not_exist_returns_404(self, api_client: APIClient):
        response = api_client.get(reverse("store:product-detail", args=[9999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestListProducts:

    def test_list_products_returns_200(self, api_client: APIClient, create_product):
        create_product()
        create_product()
        response = api_client.get(reverse("store:product-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2

    def test_if_products_does_not_exist_returns_404(self, api_client: APIClient):
        response = api_client.get(reverse("store:product-list"))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0
        assert response.data["results"] == []


@mark.django_db
class TestDeleteProduct:

    def test_if_user_is_anonymous_returns_401(
        self, api_client: APIClient, create_product
    ):
        product = create_product()
        response = api_client.delete(reverse("store:product-detail", args=[product.id]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client: APIClient, create_product, authenticate
    ):
        product = create_product()
        authenticate(is_staff=False)
        response = api_client.delete(reverse("store:product-detail", args=[product.id]))
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_204(
        self, api_client: APIClient, create_product, authenticate
    ):
        product = create_product()
        authenticate(is_staff=True)
        response = api_client.delete(reverse("store:product-detail", args=[product.id]))
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_if_product_does_not_exist_returns_404(
        self, api_client: APIClient, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.delete(reverse("store:product-detail", args=[9999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


@mark.django_db
class TestUpdateProduct:

    def test_if_user_is_anonymous_returns_401(
        self, api_client: APIClient, create_product, product_payload: dict
    ):
        product = create_product()
        response = api_client.put(
            reverse("store:product-detail", args=[product.id]), data=product_payload
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_is_not_admin_returns_403(
        self, api_client: APIClient, create_product, product_payload: dict, authenticate
    ):
        product = create_product()
        authenticate(is_staff=False)
        response = api_client.put(
            reverse("store:product-detail", args=[product.id]), data=product_payload
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_if_user_is_admin_returns_200(
        self,
        api_client: APIClient,
        create_product,
        product_payload: dict,
        authenticate,
    ):
        product = create_product()
        authenticate(is_staff=True)
        response = api_client.put(
            reverse("store:product-detail", args=[product.id]), data=product_payload
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in product_payload.items():
            assert response.data[key] == value

    def test_if_product_does_not_exist_returns_404(
        self, api_client: APIClient, product_payload: dict, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.put(
            reverse("store:product-detail", args=[9999]), data=product_payload
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_if_payload_is_invalid_returns_400(
        self,
        api_client: APIClient,
        create_product,
        invalid_product_payload: dict,
        authenticate,
    ):
        product = create_product()
        authenticate(is_staff=True)
        response = api_client.put(
            reverse("store:product-detail", args=[product.id]),
            data=invalid_product_payload,
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data
        assert "unit_price" in response.data
        assert "collection" in response.data
        assert "inventory" in response.data

    def test_if_payload_is_valid_returns_200(
        self,
        api_client: APIClient,
        create_product,
        product_payload: dict,
        authenticate,
    ):
        product = create_product()
        authenticate(is_staff=True)
        response = api_client.put(
            reverse("store:product-detail", args=[product.id]),
            data=product_payload,
        )
        assert response.status_code == status.HTTP_200_OK
        for key, value in product_payload.items():
            assert response.data[key] == value
