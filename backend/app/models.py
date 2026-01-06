"""
Pydantic models (schemas) for request/response validation.
These models define the structure of data that our API expects and returns.
"""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from bson import ObjectId


# ============ USER MODELS ============

class UserRegister(BaseModel):
    """
    Schema for user registration.
    This is what the client sends when registering a new user.
    """
    username: str = Field(..., min_length=3, max_length=50, description="Username (3-50 characters)")
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=6, description="Password (minimum 6 characters)")


class UserLogin(BaseModel):
    """
    Schema for user login.
    This is what the client sends when logging in.
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """
    Schema for user data in responses.
    This is what we return to the client (without password).
    """
    model_config = ConfigDict(json_encoders={ObjectId: str})
    
    id: str
    username: str
    email: str


# ============ STOCK PORTFOLIO MODELS ============

class StockCreate(BaseModel):
    """
    Schema for creating a new stock entry.
    This is what the client sends when adding a stock to portfolio.
    """
    stock_name: str = Field(..., min_length=1, max_length=100, description="Name of the stock (e.g., 'AAPL', 'GOOGL')")
    quantity: float = Field(..., gt=0, description="Number of shares (must be greater than 0)")
    buy_price: float = Field(..., gt=0, description="Price per share when purchased (must be greater than 0)")


class StockUpdate(BaseModel):
    """
    Schema for updating an existing stock entry.
    All fields are optional - only provided fields will be updated.
    """
    stock_name: Optional[str] = Field(None, min_length=1, max_length=100)
    quantity: Optional[float] = Field(None, gt=0)
    buy_price: Optional[float] = Field(None, gt=0)


class StockResponse(BaseModel):
    """
    Schema for stock data in responses.
    This includes calculated fields like current value and profit/loss.
    """
    model_config = ConfigDict(json_encoders={ObjectId: str})
    
    id: str
    user_id: str
    stock_name: str
    quantity: float
    buy_price: float
    current_price: float  # For now, same as buy_price (mock data)
    total_invested: float  # quantity * buy_price
    current_value: float  # quantity * current_price
    profit_loss: float  # current_value - total_invested
    profit_loss_percentage: float  # (profit_loss / total_invested) * 100


class PortfolioSummary(BaseModel):
    """
    Schema for portfolio summary (total investment, current value, etc.)
    """
    total_stocks: int
    total_invested: float
    total_current_value: float
    total_profit_loss: float
    total_profit_loss_percentage: float
    stocks: list[StockResponse]


# ============ AUTH RESPONSE MODELS ============

class TokenResponse(BaseModel):
    """
    Schema for JWT token response after login/register.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    """
    Generic message response for success/error messages.
    """
    message: str

