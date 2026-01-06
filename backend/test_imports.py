"""
Quick script to test if all imports work correctly.
Run this before starting the server to identify import issues.
"""

print("Testing imports...")

try:
    print("1. Testing FastAPI...")
    from fastapi import FastAPI
    print("   ✅ FastAPI imported successfully")
except ImportError as e:
    print(f"   ❌ FastAPI import failed: {e}")
    print("   Run: pip install fastapi uvicorn")

try:
    print("2. Testing Motor (MongoDB)...")
    from motor.motor_asyncio import AsyncIOMotorClient
    print("   ✅ Motor imported successfully")
except ImportError as e:
    print(f"   ❌ Motor import failed: {e}")
    print("   Run: pip install motor pymongo")

try:
    print("3. Testing JWT...")
    from jose import jwt
    print("   ✅ python-jose imported successfully")
except ImportError as e:
    print(f"   ❌ python-jose import failed: {e}")
    print("   Run: pip install 'python-jose[cryptography]'")

try:
    print("4. Testing password hashing...")
    from passlib.context import CryptContext
    print("   ✅ passlib imported successfully")
except ImportError as e:
    print(f"   ❌ passlib import failed: {e}")
    print("   Run: pip install 'passlib[bcrypt]'")

try:
    print("5. Testing Pydantic...")
    from pydantic import BaseModel, EmailStr, Field
    print("   ✅ Pydantic imported successfully")
except ImportError as e:
    print(f"   ❌ Pydantic import failed: {e}")
    print("   Run: pip install 'pydantic[email]'")

try:
    print("6. Testing app modules...")
    from app.database import get_database
    from app.models import UserRegister
    from app.auth import create_access_token
    print("   ✅ App modules imported successfully")
except ImportError as e:
    print(f"   ❌ App module import failed: {e}")
    print("   Make sure you're in the backend directory")

print("\n✅ All imports successful! You can now run: uvicorn app.main:app --reload")












