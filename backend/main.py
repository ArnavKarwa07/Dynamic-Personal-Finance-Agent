from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import router as api_router
from config.settings import settings
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="Personal Finance Agent API",
    description="LangGraph-based Personal Finance Agent with comprehensive financial analysis tools",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Personal Finance Agent API",
        "version": "1.0.0",
        "description": "LangGraph-based AI agent for comprehensive financial analysis",
        "endpoints": {
            "chat": "/api/v1/chat",
            "workflow": "/api/v1/workflow", 
            "examples": "/api/v1/examples",
            "health": "/api/v1/health",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host=settings.api_host, 
        port=settings.api_port,
        reload=settings.debug
    )