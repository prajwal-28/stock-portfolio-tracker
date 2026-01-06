"""
Pytest configuration and shared fixtures.
This file contains fixtures that can be used across all test files.
"""

import pytest
import httpx
from typing import AsyncGenerator

# Base URL for the FastAPI backend
BASE_URL = "http://127.0.0.1:8000"

# Test user credentials
TEST_USERNAME = "testuser_api"
TEST_EMAIL = "testuser_api@example.com"
TEST_PASSWORD = "testpass123"


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    Create an async HTTP client for making API requests.
    This client is used for all API tests.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as ac:
        yield ac


@pytest.fixture
async def auth_token(client: httpx.AsyncClient) -> str:
    """
    Register a new user and return the JWT token.
    This fixture ensures we have a valid token for protected route tests.
    
    If registration fails (user already exists), try to login instead.
    """
    # Try to register first
    register_data = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    try:
        # Try registration
        response = await client.post("/api/auth/register", json=register_data)
        if response.status_code == 201:
            data = response.json()
            token = data["access_token"]
            if token:
                return token
    except Exception:
        pass
    
    # If registration fails, try login
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    response = await client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    
    data = response.json()
    token = data["access_token"]
    assert token is not None, "Token should not be None"
    
    return token


@pytest.fixture
async def authenticated_client(auth_token: str) -> AsyncGenerator[httpx.AsyncClient, None]:
    """
    Create an authenticated HTTP client with JWT token in headers.
    Use this for testing protected routes.
    """
    # Create a new client with the authorization header
    headers = {"Authorization": f"Bearer {auth_token}"}
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0, headers=headers) as ac:
        yield ac

