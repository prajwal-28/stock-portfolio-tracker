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
        
    Example:
        >>> simulate_stock_price('AAPL', 150.00)
        152.34  # Price between 142.50 and 157.50 (±5% of 150.00)
    """
    # Validate inputs
    if buy_price <= 0:
        return buy_price
    
    # Create a deterministic seed based on stock name and current hour
    # This ensures the same stock has consistent price within the same hour
    # but changes over time to simulate market movement
    current_hour = int(time.time() // 3600)  # Changes every hour
    seed_string = f"{stock_name}_{current_hour}"
    
    # Generate a hash from the seed to get a pseudo-random number
    hash_object = hashlib.md5(seed_string.encode())
    hash_hex = hash_object.hexdigest()
    
    # Convert first 8 characters of hash to a number between 0 and 1
    hash_int = int(hash_hex[:8], 16)
    random_factor = (hash_int % 10000) / 10000.0  # Value between 0 and 1
    
    # Calculate price variation: ±5% of buy_price
    # Map random_factor (0-1) to variation range (-0.05 to +0.05)
    variation_percent = (random_factor - 0.5) * 0.10  # Range: -0.05 to +0.05
    
    # Calculate simulated price
    simulated_price = buy_price * (1 + variation_percent)
    
    # Ensure price is always positive (safety check)
    if simulated_price <= 0:
        simulated_price = buy_price
    
    # Round to 2 decimal places
    return round(simulated_price, 2)










