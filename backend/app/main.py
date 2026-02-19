"""
Main FastAPI application file.
This is the entry point of the backend application.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, portfolio

# Create FastAPI application instance
app = FastAPI(
    title="Stock Portfolio Tracker API",
    description="A simple API for tracking stock portfolios",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the frontend to make requests to the backend
app.add_middleware(
    CORSMiddleware,
    # Local dev + deployed frontend origins.
    #
    # Note: Vercel preview deployments use different subdomains, so we also allow
    # any `*.vercel.app` origin via `allow_origin_regex`.
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://stock-portfolio-tracker-khaki.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Startup event - runs when the application starts
@app.on_event("startup")
async def startup_event():
    """
    Initialize database connection when the application starts.
    """
    await connect_to_mongo()


# Shutdown event - runs when the application shuts down
@app.on_event("shutdown")
async def shutdown_event():
    """
    Close database connection when the application shuts down.
    """
    await close_mongo_connection()


# Include routers
# This connects our route files to the main application
app.include_router(auth.router)
app.include_router(portfolio.router)


# Root endpoint - just a welcome message
@app.get("/")
async def root():
    """
    Root endpoint - returns a welcome message.
    """
    return {
        "message": "Welcome to Stock Portfolio Tracker API",
        "docs": "/docs",
        "version": "1.0.0"
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy"}












