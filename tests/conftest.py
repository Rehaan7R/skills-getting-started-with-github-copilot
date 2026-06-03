"""Shared pytest fixtures for FastAPI tests"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient for making HTTP requests to the FastAPI app.
    Uses httpx.TestClient for testing without running an actual server.
    """
    return TestClient(app)
