"""
Portfolio routes.
Handles CRUD operations for stock portfolio.
All routes require authentication (JWT token).
"""

from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from typing import List
from datetime import datetime
from app.database import get_database
from app.models import (
    StockCreate, 
    StockUpdate, 
    StockResponse, 
    PortfolioSummary,
    MessageResponse
)
from app.routes.auth import get_current_user
from app.utils.price_simulator import simulate_stock_price

# Create router for portfolio endpoints
router = APIRouter(prefix="/api/portfolio", tags=["Portfolio"])


def calculate_stock_metrics(quantity: float, buy_price: float, current_price: float) -> dict:
    """
    Calculate stock metrics: total invested, current value, profit/loss.
    
    Args:
        quantity: Number of shares
        buy_price: Price per share when purchased
        current_price: Current price per share (mock data for now)
        
    Returns:
        Dictionary with calculated metrics
    """
    total_invested = quantity * buy_price
    current_value = quantity * current_price
    profit_loss = current_value - total_invested
    profit_loss_percentage = (profit_loss / total_invested * 100) if total_invested > 0 else 0
    
    return {
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "profit_loss": round(profit_loss, 2),
        "profit_loss_percentage": round(profit_loss_percentage, 2)
    }


@router.post("/stocks", response_model=StockResponse, status_code=status.HTTP_201_CREATED)
async def add_stock(
    stock_data: StockCreate,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Add a new stock to the user's portfolio.
    
    Steps:
    1. Get current user from JWT token
    2. Use buy_price as current_price (mock data)
    3. Calculate metrics
    4. Save to database
    5. Return stock data with calculations
    """
    user_id = str(current_user["_id"])
    
    # For now, use buy_price as current_price (mock data)
    # In a real app, you would fetch current price from an API
    current_price = stock_data.buy_price
    
    # Calculate metrics
    metrics = calculate_stock_metrics(
        stock_data.quantity,
        stock_data.buy_price,
        current_price
    )
    
    # Create stock document
    stock_doc = {
        "user_id": user_id,
        "stock_name": stock_data.stock_name,
        "quantity": stock_data.quantity,
        "buy_price": stock_data.buy_price,
        "current_price": current_price,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    # Insert into database
    result = await db.portfolio.insert_one(stock_doc)
    
    # Return stock response with all calculated fields
    return StockResponse(
        id=str(result.inserted_id),
        user_id=user_id,
        stock_name=stock_data.stock_name,
        quantity=stock_data.quantity,
        buy_price=stock_data.buy_price,
        current_price=current_price,
        **metrics
    )


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
    stocks = await cursor.to_list(length=1000)  # Limit to 1000 stocks
    
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


@router.get("/stocks/{stock_id}", response_model=StockResponse)
async def get_stock(
    stock_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Get a specific stock by ID.
    
    Only returns the stock if it belongs to the current user.
    """
    user_id = str(current_user["_id"])
    
    # Validate ObjectId format
    if not ObjectId.is_valid(stock_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid stock ID format"
        )
    
    # Find the stock
    stock = await db.portfolio.find_one({
        "_id": ObjectId(stock_id),
        "user_id": user_id
    })
    
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )
    
    # Simulate current price dynamically (not from database)
    # Price fluctuates ±5% of buy_price to show realistic profit/loss
    current_price = simulate_stock_price(stock["stock_name"], stock["buy_price"])
    
    # Calculate metrics using simulated price
    metrics = calculate_stock_metrics(
        stock["quantity"],
        stock["buy_price"],
        current_price
    )
    
    return StockResponse(
        id=str(stock["_id"]),
        user_id=stock["user_id"],
        stock_name=stock["stock_name"],
        quantity=stock["quantity"],
        buy_price=stock["buy_price"],
        current_price=current_price,
        **metrics
    )


@router.put("/stocks/{stock_id}", response_model=StockResponse)
async def update_stock(
    stock_id: str,
    stock_data: StockUpdate,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Update an existing stock entry.
    
    Only updates fields that are provided (partial update).
    Only the owner can update their stocks.
    """
    user_id = str(current_user["_id"])
    
    # Validate ObjectId format
    if not ObjectId.is_valid(stock_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid stock ID format"
        )
    
    # Find the stock and verify ownership
    stock = await db.portfolio.find_one({
        "_id": ObjectId(stock_id),
        "user_id": user_id
    })
    
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )
    
    # Build update document (only include fields that are provided)
    update_data = {"updated_at": datetime.utcnow()}
    
    if stock_data.stock_name is not None:
        update_data["stock_name"] = stock_data.stock_name
    
    if stock_data.quantity is not None:
        update_data["quantity"] = stock_data.quantity
    
    if stock_data.buy_price is not None:
        update_data["buy_price"] = stock_data.buy_price
        # If buy_price is updated, also update current_price (mock)
        update_data["current_price"] = stock_data.buy_price
    
    # Update the stock
    await db.portfolio.update_one(
        {"_id": ObjectId(stock_id)},
        {"$set": update_data}
    )
    
    # Fetch updated stock
    updated_stock = await db.portfolio.find_one({"_id": ObjectId(stock_id)})
    
    # Simulate current price dynamically (not from database)
    # Price fluctuates ±5% of buy_price to show realistic profit/loss
    current_price = simulate_stock_price(updated_stock["stock_name"], updated_stock["buy_price"])
    
    # Calculate metrics using simulated price
    metrics = calculate_stock_metrics(
        updated_stock["quantity"],
        updated_stock["buy_price"],
        current_price
    )
    
    return StockResponse(
        id=str(updated_stock["_id"]),
        user_id=updated_stock["user_id"],
        stock_name=updated_stock["stock_name"],
        quantity=updated_stock["quantity"],
        buy_price=updated_stock["buy_price"],
        current_price=current_price,
        **metrics
    )


@router.delete("/stocks/{stock_id}", response_model=MessageResponse)
async def delete_stock(
    stock_id: str,
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Delete a stock from the portfolio.
    
    Only the owner can delete their stocks.
    """
    user_id = str(current_user["_id"])
    
    # Validate ObjectId format
    if not ObjectId.is_valid(stock_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid stock ID format"
        )
    
    # Find and delete the stock (only if it belongs to the user)
    result = await db.portfolio.delete_one({
        "_id": ObjectId(stock_id),
        "user_id": user_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock not found"
        )
    
    return MessageResponse(message="Stock deleted successfully")


@router.get("/summary", response_model=PortfolioSummary)
async def get_portfolio_summary(
    current_user = Depends(get_current_user),
    db = Depends(get_database)
):
    """
    Get portfolio summary with totals.
    
    Calculates:
    - Total number of stocks
    - Total invested amount
    - Total current value
    - Total profit/loss
    - Total profit/loss percentage
    - List of all stocks
    """
    user_id = str(current_user["_id"])
    
    # Get all stocks for this user
    cursor = db.portfolio.find({"user_id": user_id})
    stocks = await cursor.to_list(length=1000)
    
    # Initialize totals
    total_invested = 0
    total_current_value = 0
    stock_list = []
    
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
        
        total_invested += metrics["total_invested"]
        total_current_value += metrics["current_value"]
        
        stock_list.append(StockResponse(
            id=str(stock["_id"]),
            user_id=stock["user_id"],
            stock_name=stock["stock_name"],
            quantity=stock["quantity"],
            buy_price=stock["buy_price"],
            current_price=current_price,
            **metrics
        ))
    
    # Calculate overall profit/loss
    total_profit_loss = total_current_value - total_invested
    total_profit_loss_percentage = (
        (total_profit_loss / total_invested * 100) if total_invested > 0 else 0
    )
    
    return PortfolioSummary(
        total_stocks=len(stock_list),
        total_invested=round(total_invested, 2),
        total_current_value=round(total_current_value, 2),
        total_profit_loss=round(total_profit_loss, 2),
        total_profit_loss_percentage=round(total_profit_loss_percentage, 2),
        stocks=stock_list
    )

