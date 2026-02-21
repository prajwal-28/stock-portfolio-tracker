"""
Authentication routes.
Handles user registration and login.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database import get_database
from app.models import UserRegister, UserLogin, TokenResponse, UserResponse, MessageResponse
from app.auth import verify_password, get_password_hash, create_access_token, verify_token
from bson import ObjectId
from datetime import datetime, timedelta

# Create router for authentication endpoints
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Security scheme for JWT token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db = Depends(get_database)
):
    """
    Dependency function to get the current authenticated user.
    This extracts the JWT token from the request and validates it.
    
    Args:
        credentials: HTTPBearer credentials containing the token
        db: Database dependency
        
    Returns:
        User document from database
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    # Get token from credentials
    token = credentials.credentials
    
    # Verify the token
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user_id from token payload
    user_id = payload.get("sub")  # 'sub' is the standard JWT claim for subject (user_id)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Find user in database
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db = Depends(get_database)):
    """
    Register a new user.
    """
    # Check if username already exists
    existing_user = await db.users.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = await db.users.find_one({"email": user_data.email})
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password before storing
    hashed_password = get_password_hash(user_data.password)
    
    # Create user document
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    }
    
    # Insert user into database
    result = await db.users.insert_one(user_doc)
    
    # Create JWT token
    # 'sub' (subject) is a standard JWT claim that typically contains the user identifier
    token_data = {"sub": str(result.inserted_id), "username": user_data.username}
    access_token = create_access_token(data=token_data)
    
    # Return token and user info
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(result.inserted_id),
            username=user_data.username,
            email=user_data.email
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db = Depends(get_database)):
    """
    Login an existing user.
    
    Steps:
    1. Find user by username
    2. Verify password
    3. Create JWT token
    4. Return token and user info
    """
    # Find user by username
    user = await db.users.find_one({"username": user_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Verify password
    if not verify_password(user_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Create JWT token
    token_data = {"sub": str(user["_id"]), "username": user["username"]}
    access_token = create_access_token(data=token_data)
    
    # Return token and user info
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=str(user["_id"]),
            username=user["username"],
            email=user["email"]
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """
    Get current authenticated user's information.
    This endpoint is protected and requires a valid JWT token.
    """
    return UserResponse(
        id=str(current_user["_id"]),
        username=current_user["username"],
        email=current_user["email"]
    )

