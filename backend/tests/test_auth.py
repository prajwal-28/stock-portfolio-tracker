"""
Tests for authentication endpoints.
Tests user registration, login, and JWT token functionality.
"""

import pytest
import httpx
import time
from tests.conftest import TEST_USERNAME, TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio
async def test_user_registration(client: httpx.AsyncClient):
    """
    Test user registration endpoint.
    Creates a new user and verifies JWT token is returned.
    """
    # Generate unique username/email for this test
    import time
    unique_id = int(time.time())
    register_data = {
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "testpass123"
    }
    
    # Make registration request
    response = await client.post("/api/auth/register", json=register_data)
    
    # Should return 201 Created
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Should contain access_token
    assert "access_token" in data, "Response should contain 'access_token'"
    assert data["access_token"] is not None, "Token should not be None"
    assert len(data["access_token"]) > 0, "Token should not be empty"
    
    # Should contain token_type
    assert "token_type" in data, "Response should contain 'token_type'"
    assert data["token_type"] == "bearer", f"Token type should be 'bearer', got '{data['token_type']}'"
    
    # Should contain user info
    assert "user" in data, "Response should contain 'user'"
    user = data["user"]
    assert "id" in user, "User should have 'id'"
    assert "username" in user, "User should have 'username'"
    assert "email" in user, "User should have 'email'"
    assert user["username"] == register_data["username"], "Username should match"


@pytest.mark.asyncio
async def test_user_registration_duplicate_username(client: httpx.AsyncClient):
    """
    Test that registering with an existing username returns an error.
    """
    # First registration
    register_data = {
        "username": f"duplicate_test_{int(time.time())}",
        "email": f"duplicate_test_{int(time.time())}@example.com",
        "password": "testpass123"
    }
    
    response1 = await client.post("/api/auth/register", json=register_data)
    assert response1.status_code == 201, "First registration should succeed"
    
    # Try to register again with same username
    response2 = await client.post("/api/auth/register", json=register_data)
    
    # Should return 400 Bad Request
    assert response2.status_code == 400, f"Expected 400 for duplicate username, got {response2.status_code}"
    
    # Should contain error message
    data = response2.json()
    assert "detail" in data, "Error response should contain 'detail'"
    assert "already" in data["detail"].lower(), "Error should mention username already exists"


@pytest.mark.asyncio
async def test_user_login(client: httpx.AsyncClient, auth_token: str):
    """
    Test user login endpoint.
    Verifies that login returns a valid JWT token.
    """
    login_data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    # Make login request
    response = await client.post("/api/auth/login", json=login_data)
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Should contain access_token
    assert "access_token" in data, "Response should contain 'access_token'"
    assert data["access_token"] is not None, "Token should not be None"
    assert len(data["access_token"]) > 0, "Token should not be empty"
    
    # Should contain user info
    assert "user" in data, "Response should contain 'user'"
    user = data["user"]
    assert user["username"] == TEST_USERNAME, "Username should match"


@pytest.mark.asyncio
async def test_user_login_invalid_credentials(client: httpx.AsyncClient):
    """
    Test that login with wrong password returns an error.
    """
    login_data = {
        "username": TEST_USERNAME,
        "password": "wrongpassword123"
    }
    
    # Make login request with wrong password
    response = await client.post("/api/auth/login", json=login_data)
    
    # Should return 401 Unauthorized
    assert response.status_code == 401, f"Expected 401 for wrong password, got {response.status_code}"
    
    # Should contain error message
    data = response.json()
    assert "detail" in data, "Error response should contain 'detail'"


@pytest.mark.asyncio
async def test_get_current_user_with_token(client: httpx.AsyncClient, auth_token: str):
    """
    Test accessing protected route /api/auth/me with JWT token.
    Verifies that JWT authentication is working.
    """
    # Set authorization header
    headers = {"Authorization": f"Bearer {auth_token}"}
    
    # Make request to protected endpoint
    response = await client.get("/api/auth/me", headers=headers)
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Should contain user info
    assert "id" in data, "Response should contain 'id'"
    assert "username" in data, "Response should contain 'username'"
    assert "email" in data, "Response should contain 'email'"
    assert data["username"] == TEST_USERNAME, "Username should match"


@pytest.mark.asyncio
async def test_get_current_user_without_token(client: httpx.AsyncClient):
    """
    Test that accessing protected route without token returns 401.
    """
    # Make request without authorization header
    response = await client.get("/api/auth/me")
    
    # Should return 401 Unauthorized
    assert response.status_code == 401, f"Expected 401 without token, got {response.status_code}"


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token(client: httpx.AsyncClient):
    """
    Test that accessing protected route with invalid token returns 401.
    """
    # Set invalid authorization header
    headers = {"Authorization": "Bearer invalid_token_12345"}
    
    # Make request with invalid token
    response = await client.get("/api/auth/me", headers=headers)
    
    # Should return 401 Unauthorized
    assert response.status_code == 401, f"Expected 401 with invalid token, got {response.status_code}"

