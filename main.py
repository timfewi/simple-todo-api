"""
Simple Todo API - FastAPI Application

A learning project demonstrating FastAPI best practices for building REST APIs.
This Todo API includes CRUD operations, data validation, and proper error handling.
"""

import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import todos

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for handling startup and shutdown events.

    This replaces the deprecated @app.on_event decorators and provides
    a more modern approach to handling application lifecycle events.
    """
    yield
    # Shutdown: Add any cleanup logic here if needed
    # (currently no cleanup is required for this application)


# Create FastAPI application instance with lifespan handler
app = FastAPI(
    title=os.getenv("API_TITLE", "Simple Todo API"),
    description=os.getenv(
        "API_DESCRIPTION", "A FastAPI learning project for managing todo items"
    ),
    version=os.getenv("API_VERSION", "1.0.0"),
    docs_url="/docs" if os.getenv("DOCS_ENABLED", "true").lower() == "true" else None,
    redoc_url=(
        "/redoc" if os.getenv("REDOC_ENABLED", "true").lower() == "true" else None
    ),
    lifespan=lifespan,
)

# Configure CORS middleware for frontend integration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
allowed_methods = os.getenv("ALLOWED_METHODS", "*").split(",")
allowed_headers = os.getenv("ALLOWED_HEADERS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins],
    allow_credentials=True,
    allow_methods=[method.strip() for method in allowed_methods],
    allow_headers=[header.strip() for header in allowed_headers],
)

# Include API routers
app.include_router(todos.router, prefix="/api/v1", tags=["todos"])


@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.

    Returns:
        dict: Welcome message and API documentation links
    """
    return {
        "message": "Welcome to Simple Todo API",
        "version": os.getenv("API_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "documentation": {"swagger": "/docs", "redoc": "/redoc"},
        "endpoints": {"todos": "/api/v1/todos", "health": "/health"},
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Service health status
    """
    return {
        "status": "healthy",
        "service": "simple-todo-api",
        "version": os.getenv("API_VERSION", "1.0.0"),
        "environment": os.getenv("ENVIRONMENT", "development"),
    }
