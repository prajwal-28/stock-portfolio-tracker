# Price Simulator - Before/After Code Comparison

## NEW FILE: `backend/app/utils/price_simulator.py`

```python
"""
Stock Price Simulator Utility

This module provides simulated stock prices for demonstration purposes.
Since we're not using real stock APIs, this generates realistic price fluctuations
based on the buy_price.

IMPORTANT: This is a DUMMY/SIMULATED price generator for educational purposes.
In a production environment, you would fetch real-time prices from a stock API.

The simulation:
- Generates prices that fluctuate within ±5% of the buy_price
- Uses deterministic randomness based on stock_name for consistency
- Returns prices rounded to 2 decimal places
- Ensures prices are always positive
"""

import hashlib
import time


def simulate_stock_price(stock_name: str, buy_price: float) -> float:
    """
    Simulate a current stock price based on buy_price.
    
    This function generates a price that fluctuates within ±5% of the buy_price.
    The price is deterministic based on stock_name and current time (hourly variation),
    so the same stock will have the same price within the same hour, but will change
    over time to simulate market fluctuations.
    
    Args:
        stock_name: Name of the stock (e.g., 'AAPL', 'GOOGL')
        buy_price: The original purchase price of the stock
        
    Returns:
        Simulated current price (rounded to 2 decimal places)
    """
    # Validate inputs
    if buy_price <= 0:
        return buy_price
    
    # Create a deterministic seed based on stock name and current hour
    current_hour = int(time.time() // 3600)  # Changes every hour
    seed_string = f"{stock_name}_{current_hour}"
    
    # Generate a hash from the seed to get a pseudo-random number
    hash_object = hashlib.md5(seed_string.encode())
    hash_hex = hash_object.hexdigest()
    
    # Convert first 8 characters of hash to a number between 0 and 1
    hash_int = int(hash_hex[:8], 16)
    random_factor = (hash_int % 10000) / 10000.0  # Value between 0 and 1
    
    # Calculate price variation: ±5% of buy_price
    variation_percent = (random_factor - 0.5) * 0.10  # Range: -0.05 to +0.05
    
    # Calculate simulated price
    simulated_price = buy_price * (1 + variation_percent)
    
    # Ensure price is always positive
    if simulated_price <= 0:
        simulated_price = buy_price
    
    # Round to 2 decimal places
    return round(simulated_price, 2)
```

---

## MODIFIED: `backend/app/routes/portfolio.py`

### Change 1: Added Import

**BEFORE:**
```python
from app.routes.auth import get_current_user
```

**AFTER:**
```python
from app.routes.auth import get_current_user
from app.utils.price_simulator import simulate_stock_price
```

---

### Change 2: GET /api/portfolio/stocks

**BEFORE:**
```python
@router.get("/stocks", response_model=List[StockResponse])
async def get_all_stocks(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Get all stocks in the user's portfolio.
    
    Returns a list of all stocks with calculated metrics.
    """
    user_id = str(current_user["_id"])
    
    # Find all stocks for this user
    cursor = db.portfolio.find({"user_id": user_id})
    stocks = await cursor.to_list(length=1000)
    
    # Convert to response format
    stock_list = []
    for stock in stocks:
        # Recalculate metrics (in case current_price changed)
        metrics = calculate_stock_metrics(
            stock["quantity"],
            stock["buy_price"],
            stock.get("current_price", stock["buy_price"])
        )
        
        stock_list.append(StockResponse(
            id=str(stock["_id"]),
            user_id=stock["user_id"],
            stock_name=stock["stock_name"],
            quantity=stock["quantity"],
            buy_price=stock["buy_price"],
            current_price=stock.get("current_price", stock["buy_price"]),
            **metrics
        ))
    
    return stock_list
```

**AFTER:**
```python
@router.get("/stocks", response_model=List[StockResponse])
async def get_all_stocks(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Get all stocks in the user's portfolio.
    
    Returns a list of all stocks with calculated metrics.
    Current prices are simulated dynamically (not stored in database).
    """
    user_id = str(current_user["_id"])
    
    # Find all stocks for this user
    cursor = db.portfolio.find({"user_id": user_id})
    stocks = await cursor.to_list(length=1000)
    
    # Convert to response format
    stock_list = []
    for stock in stocks:
        # Simulate current price dynamically (not from database)
        # Price fluctuates ±5% of buy_price to show realistic profit/loss
        current_price = simulate_stock_price(stock["stock_name"], stock["buy_price"])
        
        # Calculate metrics using simulated price
        metrics = calculate_stock_metrics(
            stock["quantity"],
            stock["buy_price"],
            current_price
        )
        
        stock_list.append(StockResponse(
            id=str(stock["_id"]),
            user_id=stock["user_id"],
            stock_name=stock["stock_name"],
            quantity=stock["quantity"],
            buy_price=stock["buy_price"],
            current_price=current_price,
            **metrics
        ))
    
    return stock_list
```

---

### Change 3: GET /api/portfolio/stocks/{stock_id}

**BEFORE:**
```python
    # Calculate metrics
    current_price = stock.get("current_price", stock["buy_price"])
    metrics = calculate_stock_metrics(
        stock["quantity"],
        stock["buy_price"],
        current_price
    )
```

**AFTER:**
```python
    # Simulate current price dynamically (not from database)
    # Price fluctuates ±5% of buy_price to show realistic profit/loss
    current_price = simulate_stock_price(stock["stock_name"], stock["buy_price"])
    
    # Calculate metrics using simulated price
    metrics = calculate_stock_metrics(
        stock["quantity"],
        stock["buy_price"],
        current_price
    )
```

---

### Change 4: GET /api/portfolio/summary

**BEFORE:**
```python
    # Calculate for each stock
    for stock in stocks:
        current_price = stock.get("current_price", stock["buy_price"])
        metrics = calculate_stock_metrics(
            stock["quantity"],
            stock["buy_price"],
            current_price
        )
```

**AFTER:**
```python
    # Calculate for each stock
    for stock in stocks:
        # Simulate current price dynamically (not from database)
        # Price fluctuates ±5% of buy_price to show realistic profit/loss
        current_price = simulate_stock_price(stock["stock_name"], stock["buy_price"])
        
        # Calculate metrics using simulated price
        metrics = calculate_stock_metrics(
            stock["quantity"],
            stock["buy_price"],
            current_price
        )
```

---

### Change 5: PUT /api/portfolio/stocks/{stock_id} (Response Only)

**BEFORE:**
```python
    # Calculate metrics
    current_price = updated_stock.get("current_price", updated_stock["buy_price"])
    metrics = calculate_stock_metrics(
        updated_stock["quantity"],
        updated_stock["buy_price"],
        current_price
    )
```

**AFTER:**
```python
    # Simulate current price dynamically (not from database)
    # Price fluctuates ±5% of buy_price to show realistic profit/loss
    current_price = simulate_stock_price(updated_stock["stock_name"], updated_stock["buy_price"])
    
    # Calculate metrics using simulated price
    metrics = calculate_stock_metrics(
        updated_stock["quantity"],
        updated_stock["buy_price"],
        current_price
    )
```

---

## UNCHANGED: POST /api/portfolio/stocks

**NO CHANGES** - Still uses buy_price as current_price in response (appropriate for newly added stock)

```python
# This remains unchanged - newly added stock has current_price = buy_price
current_price = stock_data.buy_price
```

---

## Summary

- ✅ Created new utility module for price simulation
- ✅ Modified 4 GET/PUT response endpoints to use simulator
- ✅ POST endpoint unchanged (new stocks start at buy_price)
- ✅ Database operations unchanged
- ✅ No frontend changes needed
- ✅ No authentication changes
- ✅ No database schema changes










