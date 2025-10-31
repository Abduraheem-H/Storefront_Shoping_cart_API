import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    """Fixture for DRF test client."""
    return APIClient()


@pytest.fixture
def collection_payload():
    """Fixture for sample collection data."""
    return {"title": "My Test Collection"}


@pytest.fixture
def authenticate(api_client):
    """Fixture to authenticate a user."""

    def _authenticate(is_staff=False):
        return api_client.force_authenticate(user=User(is_staff=is_staff))

    return _authenticate
