from requests import get
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from pytest import mark
from django.contrib.auth.models import User


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
