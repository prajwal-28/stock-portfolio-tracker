"""
Tests for health check and basic API endpoints.
These tests verify that the FastAPI server is running and responding.
"""

import pytest
import httpx


BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_root_endpoint():
    """
    Test the root endpoint (/) returns a welcome message.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        response = await client.get("/")
        
        # Should return 200 OK
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Should return JSON with message
        data = response.json()
        assert "message" in data, "Response should contain 'message' field"
        assert "Stock Portfolio" in data["message"], "Message should mention Stock Portfolio"


@pytest.mark.asyncio
async def test_health_endpoint():
    """
    Test the health check endpoint (/health).
    This is used to verify the API is running.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        response = await client.get("/health")
        
        # Should return 200 OK
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Should return JSON with status
        data = response.json()
        assert "status" in data, "Response should contain 'status' field"
        assert data["status"] == "healthy", f"Status should be 'healthy', got '{data['status']}'"


@pytest.mark.asyncio
async def test_api_docs_available():
    """
    Test that API documentation is available at /docs.
    This verifies FastAPI's automatic documentation feature is working.
    """
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10.0) as client:
        response = await client.get("/docs")
        
        # Should return 200 OK (HTML page)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        # Should return HTML content
        assert "text/html" in response.headers.get("content-type", ""), "Should return HTML"










