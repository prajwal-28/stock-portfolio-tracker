"""
Tests for stock portfolio CRUD operations.
Tests adding, viewing, updating, and deleting stocks.
"""

import pytest
import httpx
from tests.conftest import TEST_USERNAME


@pytest.mark.asyncio
async def test_add_stock(authenticated_client: httpx.AsyncClient):
    """
    Test adding a stock to the portfolio.
    Verifies that stock is created with correct data and calculations.
    """
    stock_data = {
        "stock_name": "AAPL",
        "quantity": 10,
        "buy_price": 150.50
    }
    
    # Make request to add stock
    response = await authenticated_client.post("/api/portfolio/stocks", json=stock_data)
    
    # Should return 201 Created
    assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Verify all required fields are present
    assert "id" in data, "Response should contain 'id'"
    assert "user_id" in data, "Response should contain 'user_id'"
    assert "stock_name" in data, "Response should contain 'stock_name'"
    assert "quantity" in data, "Response should contain 'quantity'"
    assert "buy_price" in data, "Response should contain 'buy_price'"
    assert "current_price" in data, "Response should contain 'current_price'"
    assert "total_invested" in data, "Response should contain 'total_invested'"
    assert "current_value" in data, "Response should contain 'current_value'"
    assert "profit_loss" in data, "Response should contain 'profit_loss'"
    assert "profit_loss_percentage" in data, "Response should contain 'profit_loss_percentage'"
    
    # Verify data matches input
    assert data["stock_name"] == stock_data["stock_name"], "Stock name should match"
    assert data["quantity"] == stock_data["quantity"], "Quantity should match"
    assert data["buy_price"] == stock_data["buy_price"], "Buy price should match"
    
    # Verify calculations (current_price = buy_price for mock data)
    expected_invested = stock_data["quantity"] * stock_data["buy_price"]
    assert abs(data["total_invested"] - expected_invested) < 0.01, f"Total invested should be {expected_invested}"
    assert abs(data["current_value"] - expected_invested) < 0.01, "Current value should equal total invested (mock)"
    assert abs(data["profit_loss"]) < 0.01, "Profit/loss should be 0 (mock data)"


@pytest.mark.asyncio
async def test_get_all_stocks(authenticated_client: httpx.AsyncClient):
    """
    Test getting all stocks from portfolio.
    Verifies that the endpoint returns a list of stocks.
    """
    # First, add a stock to ensure we have data
    stock_data = {
        "stock_name": "GOOGL",
        "quantity": 5,
        "buy_price": 2000.00
    }
    await authenticated_client.post("/api/portfolio/stocks", json=stock_data)
    
    # Get all stocks
    response = await authenticated_client.get("/api/portfolio/stocks")
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Should be a list
    assert isinstance(data, list), "Response should be a list"
    
    # Should have at least one stock
    assert len(data) > 0, "Should have at least one stock"
    
    # Verify first stock has all required fields
    if len(data) > 0:
        stock = data[0]
        assert "id" in stock, "Stock should have 'id'"
        assert "stock_name" in stock, "Stock should have 'stock_name'"
        assert "quantity" in stock, "Stock should have 'quantity'"
        assert "buy_price" in stock, "Stock should have 'buy_price'"


@pytest.mark.asyncio
async def test_get_single_stock(authenticated_client: httpx.AsyncClient):
    """
    Test getting a single stock by ID.
    Verifies that we can retrieve a specific stock.
    """
    # First, add a stock
    stock_data = {
        "stock_name": "MSFT",
        "quantity": 8,
        "buy_price": 300.00
    }
    add_response = await authenticated_client.post("/api/portfolio/stocks", json=stock_data)
    assert add_response.status_code == 201, "Stock should be added successfully"
    
    # Get the stock ID from response
    added_stock = add_response.json()
    stock_id = added_stock["id"]
    
    # Get the stock by ID
    response = await authenticated_client.get(f"/api/portfolio/stocks/{stock_id}")
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Verify it's the same stock
    assert data["id"] == stock_id, "Stock ID should match"
    assert data["stock_name"] == stock_data["stock_name"], "Stock name should match"
    assert data["quantity"] == stock_data["quantity"], "Quantity should match"


@pytest.mark.asyncio
async def test_get_nonexistent_stock(authenticated_client: httpx.AsyncClient):
    """
    Test getting a stock that doesn't exist returns 404.
    """
    # Use a fake ObjectId format
    fake_id = "507f1f77bcf86cd799439011"
    
    # Try to get non-existent stock
    response = await authenticated_client.get(f"/api/portfolio/stocks/{fake_id}")
    
    # Should return 404 Not Found
    assert response.status_code == 404, f"Expected 404 for non-existent stock, got {response.status_code}"


@pytest.mark.asyncio
async def test_update_stock(authenticated_client: httpx.AsyncClient):
    """
    Test updating a stock entry.
    Verifies that we can update stock name, quantity, or buy_price.
    """
    # First, add a stock
    stock_data = {
        "stock_name": "TSLA",
        "quantity": 20,
        "buy_price": 250.00
    }
    add_response = await authenticated_client.post("/api/portfolio/stocks", json=stock_data)
    assert add_response.status_code == 201, "Stock should be added successfully"
    
    # Get the stock ID
    added_stock = add_response.json()
    stock_id = added_stock["id"]
    
    # Update the stock (partial update - only quantity)
    update_data = {
        "quantity": 25
    }
    
    response = await authenticated_client.put(f"/api/portfolio/stocks/{stock_id}", json=update_data)
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Verify update
    assert data["quantity"] == update_data["quantity"], "Quantity should be updated"
    assert data["stock_name"] == stock_data["stock_name"], "Stock name should remain unchanged"
    assert data["buy_price"] == stock_data["buy_price"], "Buy price should remain unchanged"
    
    # Verify calculations are updated
    expected_invested = update_data["quantity"] * stock_data["buy_price"]
    assert abs(data["total_invested"] - expected_invested) < 0.01, "Total invested should be recalculated"


@pytest.mark.asyncio
async def test_delete_stock(authenticated_client: httpx.AsyncClient):
    """
    Test deleting a stock from portfolio.
    Verifies that stock is removed successfully.
    """
    # First, add a stock
    stock_data = {
        "stock_name": "NVDA",
        "quantity": 15,
        "buy_price": 400.00
    }
    add_response = await authenticated_client.post("/api/portfolio/stocks", json=stock_data)
    assert add_response.status_code == 201, "Stock should be added successfully"
    
    # Get the stock ID
    added_stock = add_response.json()
    stock_id = added_stock["id"]
    
    # Delete the stock
    response = await authenticated_client.delete(f"/api/portfolio/stocks/{stock_id}")
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    assert "message" in data, "Response should contain 'message'"
    assert "deleted" in data["message"].lower(), "Message should mention deletion"
    
    # Verify stock is actually deleted (try to get it)
    get_response = await authenticated_client.get(f"/api/portfolio/stocks/{stock_id}")
    assert get_response.status_code == 404, "Stock should not exist after deletion"


@pytest.mark.asyncio
async def test_portfolio_summary(authenticated_client: httpx.AsyncClient):
    """
    Test getting portfolio summary with totals.
    Verifies that summary includes total invested, current value, profit/loss.
    """
    # Add a couple of stocks first
    stocks = [
        {"stock_name": "AMZN", "quantity": 10, "buy_price": 100.00},
        {"stock_name": "META", "quantity": 5, "buy_price": 200.00}
    ]
    
    for stock in stocks:
        response = await authenticated_client.post("/api/portfolio/stocks", json=stock)
        assert response.status_code == 201, f"Stock {stock['stock_name']} should be added"
    
    # Get portfolio summary
    response = await authenticated_client.get("/api/portfolio/summary")
    
    # Should return 200 OK
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    
    # Parse response
    data = response.json()
    
    # Verify summary fields
    assert "total_stocks" in data, "Summary should contain 'total_stocks'"
    assert "total_invested" in data, "Summary should contain 'total_invested'"
    assert "total_current_value" in data, "Summary should contain 'total_current_value'"
    assert "total_profit_loss" in data, "Summary should contain 'total_profit_loss'"
    assert "total_profit_loss_percentage" in data, "Summary should contain 'total_profit_loss_percentage'"
    assert "stocks" in data, "Summary should contain 'stocks' list"
    
    # Verify totals make sense
    assert data["total_stocks"] >= 2, "Should have at least 2 stocks"
    assert data["total_invested"] > 0, "Total invested should be positive"
    assert isinstance(data["stocks"], list), "Stocks should be a list"
    assert len(data["stocks"]) == data["total_stocks"], "Stock count should match"


@pytest.mark.asyncio
async def test_add_stock_without_auth(client: httpx.AsyncClient):
    """
    Test that adding stock without authentication returns 401.
    """
    stock_data = {
        "stock_name": "TEST",
        "quantity": 1,
        "buy_price": 100.00
    }
    
    # Try to add stock without token
    response = await client.post("/api/portfolio/stocks", json=stock_data)
    
    # Should return 401 Unauthorized
    assert response.status_code == 401, f"Expected 401 without auth, got {response.status_code}"


@pytest.mark.asyncio
async def test_add_stock_invalid_data(authenticated_client: httpx.AsyncClient):
    """
    Test that adding stock with invalid data returns validation error.
    """
    # Try to add stock with negative quantity
    invalid_data = {
        "stock_name": "INVALID",
        "quantity": -5,  # Invalid: should be > 0
        "buy_price": 100.00
    }
    
    response = await authenticated_client.post("/api/portfolio/stocks", json=invalid_data)
    
    # Should return 422 Unprocessable Entity (validation error)
    assert response.status_code == 422, f"Expected 422 for invalid data, got {response.status_code}"










