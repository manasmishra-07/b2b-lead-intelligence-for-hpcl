"""
Run the FastAPI backend server
"""
import uvicorn
from app.config.settings import settings

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting HPCL Lead Intelligence API Server")
    print("=" * 60)
    print(f"Host: {settings.API_HOST}")
    print(f"Port: {settings.API_PORT}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"API Docs: http://localhost:{settings.API_PORT}/docs")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )