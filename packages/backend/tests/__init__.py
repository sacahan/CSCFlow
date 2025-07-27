"""Test configuration and fixtures."""

import pytest


@pytest.fixture
def client():
    """Create a test client."""
    from fastapi.testclient import TestClient
    from src.main import app

    return TestClient(app)
