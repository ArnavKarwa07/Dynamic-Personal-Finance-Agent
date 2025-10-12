"""
Auth Router - Authentication and user management endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Request/Response Models
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    username: str

class UserProfile(BaseModel):
    user_id: str
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: str
    last_login: Optional[str] = None

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    User login endpoint
    """
    try:
        # Demo user credentials
        if (request.username == "demo" and request.password == "demo123") or \
           (request.username == "demo@example.com" and request.password == "demo123"):
            return AuthResponse(
                access_token="demo_jwt_token_123456789",
                token_type="bearer",
                user_id="demo_user_001",
                username="demo"
            )
        # Allow any user for demo purposes
        elif request.username and request.password:
            return AuthResponse(
                access_token=f"mock_jwt_token_{hash(request.username)}",
                token_type="bearer",
                user_id=f"user_{hash(request.username)}"[:12],
                username=request.username
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """
    User registration endpoint
    """
    try:
        # In a real implementation, create user in database
        # For now, simulate successful registration
        
        user_id = f"user_{hash(request.username)}_{hash(request.email)}"[:16]
        
        return AuthResponse(
            access_token="mock_jwt_token_new_user",
            token_type="bearer",
            user_id=user_id,
            username=request.username
        )
    
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.get("/profile/{user_id}", response_model=UserProfile)
async def get_user_profile(user_id: str):
    """
    Get user profile information
    """
    try:
        # In a real implementation, fetch from database
        # For now, return mock data
        
        return UserProfile(
            user_id=user_id,
            username="demo_user",
            email="demo@example.com", 
            full_name="Demo User",
            created_at="2024-01-01T00:00:00Z",
            last_login="2024-01-01T12:00:00Z"
        )
    
    except Exception as e:
        logger.error(f"Profile fetch error: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch profile")

@router.post("/logout")
async def logout():
    """
    User logout endpoint
    """
    try:
        # In a real implementation, invalidate the JWT token
        return {"message": "Successfully logged out"}
    
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")

@router.post("/refresh-token")
async def refresh_token():
    """
    Refresh JWT token endpoint
    """
    try:
        # In a real implementation, generate new JWT token
        return {
            "access_token": "refreshed_jwt_token_987654321",
            "token_type": "bearer"
        }
    
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(status_code=500, detail="Token refresh failed")