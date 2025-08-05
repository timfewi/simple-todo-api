"""
Development server runner with environment validation.

This script helps validate environment configuration and start the development server.
"""

import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv


def validate_env():
    """Validate critical environment variables."""
    load_dotenv()

    critical_vars = {
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "ENVIRONMENT": os.getenv("ENVIRONMENT", "development"),
    }

    missing_vars = [var for var, value in critical_vars.items() if not value]

    if missing_vars:
        print(f"❌ Missing critical environment variables: {', '.join(missing_vars)}")
        print("💡 Make sure you have a .env file with all required variables.")
        return False

    print("✅ Environment validation passed!")
    print(f"🗄️  Database: {critical_vars['DATABASE_URL']}")
    print(f"🌍 Environment: {critical_vars['ENVIRONMENT']}")
    return True


def main():
    """Run the development server."""
    if not validate_env():
        sys.exit(1)

    # Load environment variables
    load_dotenv()

    # Get server configuration from environment
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()

    print(f"🚀 Starting Simple Todo API on http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"📖 ReDoc Documentation: http://{host}:{port}/redoc")
    print(f"🔧 Auto-reload: {'enabled' if reload else 'disabled'}")
    print("-" * 50)

    # Start the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
