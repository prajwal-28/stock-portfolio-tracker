"""
Database connection module for MongoDB.
This file handles the connection to MongoDB database.
Supports both local MongoDB and MongoDB Atlas.
"""

try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    # dotenv is optional, continue without it
    pass

import os
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# MongoDB connection string - default to localhost if not set
# For MongoDB Atlas, use: mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "stock_portfolio_db")

# Global database client instance
client = None
database = None


async def connect_to_mongo():
    """
    Connect to MongoDB database.
    This function should be called when the application starts.
    Supports both local MongoDB and MongoDB Atlas (with SSL/TLS).
    """
    global client, database

    try:
        # Check if connection string is for MongoDB Atlas (mongodb+srv://)
        is_atlas = MONGODB_URL.startswith("mongodb+srv://")
        
        # For MongoDB Atlas, SSL/TLS is automatically handled by mongodb+srv://
        # For regular mongodb:// connections, we need to configure SSL
        if is_atlas:
            # MongoDB Atlas - SSL is automatic with mongodb+srv://
            client = AsyncIOMotorClient(
                MONGODB_URL,
                serverSelectionTimeoutMS=10000  # 10 seconds timeout for Atlas
            )
        else:
            # Local MongoDB or mongodb:// connection
            # Check if connection string already has SSL parameters
            if "ssl=true" in MONGODB_URL.lower() or "tls=true" in MONGODB_URL.lower():
                # SSL already specified in connection string
                client = AsyncIOMotorClient(
                    MONGODB_URL,
                    serverSelectionTimeoutMS=5000
                )
            else:
                # No SSL specified - assume local MongoDB without SSL
                client = AsyncIOMotorClient(
                    MONGODB_URL,
                    serverSelectionTimeoutMS=5000
                )

        # Test the connection
        await client.admin.command("ping")

        # Get database
        database = client[DATABASE_NAME]

        print(f"✅ Successfully connected to MongoDB database: {DATABASE_NAME}")
        return database

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        error_msg = str(e)
        print(f"❌ Failed to connect to MongoDB")
        
        # Provide helpful error messages based on error type
        if "SSL" in error_msg or "TLS" in error_msg:
            print(f"   SSL/TLS connection error detected.")
            print(f"   For MongoDB Atlas, make sure you're using: mongodb+srv://...")
            print(f"   Example: mongodb+srv://username:password@cluster.mongodb.net/")
            print(f"   Also check:")
            print(f"   1. Your IP address is whitelisted in Atlas")
            print(f"   2. Your username and password are correct")
            print(f"   3. Your connection string uses mongodb+srv:// (not mongodb://)")
        else:
            print(f"   Error: {error_msg}")
            print(f"   Make sure MongoDB is running or your connection string is correct")
        
        raise

    except Exception as e:
        print(f"❌ Unexpected error connecting to MongoDB: {e}")
        print(f"   Error type: {type(e).__name__}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection.
    This function should be called when the application shuts down.
    """
    global client

    if client:
        client.close()
        print("✅ MongoDB connection closed")


def get_database():
    """
    Get the database instance.
    Returns the database object if connected.
    Raises an error if database is not connected.
    """
    if database is None:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Database not connected. Make sure MongoDB connection is established.")
    return database
