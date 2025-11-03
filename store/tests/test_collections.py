from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
from pytest import mark


@mark.django_db
class TestCreateCollection:
    # Test for anonymous user access
    def test_if_user_is_anonymous_returns_401(
        self, api_client: APIClient, collection_payload: dict
    ):
        response = api_client.post(
            reverse("store:collection-list"), data=collection_payload
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # Test for authenticated non-admin user access
    def test_if_user_is_not_admin_returns_403(
        self, api_client: APIClient, collection_payload: dict, authenticate
    ):
        authenticate(is_staff=False)
        response = api_client.post(
            reverse("store:collection-list"), data=collection_payload
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    # Test for authenticated admin user access
    def test_if_user_is_admin_returns_201(
        self, api_client: APIClient, collection_payload: dict, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.post(
            reverse("store:collection-list"), data=collection_payload
        )
        assert response.status_code == status.HTTP_201_CREATED

    # Test for invalid payload
    def test_if_payload_is_invalid_returns_400(
        self, api_client: APIClient, authenticate
    ):
        authenticate(is_staff=True)
        invalid_payload = {
            "title": ""
        }  # Giving an empty title to trigger validation error
        response = api_client.post(
            reverse("store:collection-list"), data=invalid_payload
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "title" in response.data

    # Test for valid payload
    def test_if_payload_is_valid_returns_201(
        self, api_client: APIClient, collection_payload: dict, authenticate
    ):
        authenticate(is_staff=True)
        response = api_client.post(
            reverse("store:collection-list"), data=collection_payload
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"] > 0


@mark.django_db
class TestRetrieveCollection:

    def test_if_collection_exists_returns_200(self, api_client: APIClient):
        collection = baker.make("store.Collection")
        response = api_client.get(
            reverse("store:collection-detail", args=[collection.id])
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "product_count": 0,
        }

    def test_if_collection_does_not_exist_returns_404(self, api_client: APIClient):
        response = api_client.get(reverse("store:collection-detail", args=[999]))
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestDeleteCollection:
    @mark.django_db
    def test_if_collection_has_products_returns_405(
        self, api_client: APIClient, authenticate
    ):
        authenticate(is_staff=True)
        collection = baker.make("store.Collection")
        baker.make("store.Product", collection=collection, _quantity=1)

        response = api_client.delete(
            reverse("store:collection-detail", args=[collection.id])
        )
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
        assert response.data["error"] == (
            "Collection cannot be deleted because it includes one or more products."
        )

    @mark.django_db
    def test_if_collection_has_no_products_returns_204(
        self, api_client: APIClient, authenticate
    ):
        authenticate(is_staff=True)
        collection = baker.make("store.Collection")

        response = api_client.delete(
            reverse("store:collection-detail", args=[collection.id])
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.data is None

    @mark.django_db
    def test_if_user_is_not_admin_returns_403_on_delete(
        self, api_client: APIClient, authenticate
    ):
        authenticate(is_staff=False)
        collection = baker.make("store.Collection")

        response = api_client.delete(
            reverse("store:collection-detail", args=[collection.id])
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestListCollections:
    @mark.django_db
    def test_list_collections_returns_200(self, api_client: APIClient):
        baker.make("store.Collection", _quantity=3)

        response = api_client.get(reverse("store:collection-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3


class TestUpdateCollection:
    @mark.django_db
    def test_update_collection_returns_200(self, api_client: APIClient, authenticate):
        authenticate(is_staff=True)
        collection = baker.make("store.Collection")
        updated_data = {"title": "Updated Collection Title"}

        response = api_client.put(
            reverse("store:collection-detail", args=[collection.id]),
            data=updated_data,
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["title"] == updated_data["title"]

    @mark.django_db
    def test_if_user_is_not_admin_returns_403_on_update(
        self, api_client: APIClient, authenticate
    ):
        authenticate(is_staff=False)
        collection = baker.make("store.Collection")
        updated_data = {"title": "Updated Collection Title"}

        response = api_client.put(
            reverse("store:collection-detail", args=[collection.id]),
            data=updated_data,
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
