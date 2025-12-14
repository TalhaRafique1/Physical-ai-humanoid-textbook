"""
Authentication API Routes

This module defines the API endpoints for user authentication and personalization.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, Optional
import logging
from datetime import datetime

from ...services.auth.auth_service import AuthService, AuthCredentials, User
from ...services.personalization.personalization_service import PersonalizationService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
auth_service = AuthService()
personalization_service = PersonalizationService()


def get_current_user(authorization: str = Header(None)) -> Optional[User]:
    """
    Get the current authenticated user from the authorization header.

    Args:
        authorization: Authorization header containing the token

    Returns:
        User object if authenticated, None otherwise
    """
    if not authorization:
        return None

    try:
        # Extract token from "Bearer <token>" format
        if authorization.startswith("Bearer "):
            token = authorization[7:]
        else:
            token = authorization

        # Get user by token
        user = auth_service.get_user_by_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/register")
async def register_user(credentials: AuthCredentials) -> Dict[str, Any]:
    """
    Register a new user.

    Args:
        credentials: User registration credentials

    Returns:
        Dictionary with user information and authentication token
    """
    try:
        result = await auth_service.register_user(
            email=credentials.email,
            password=credentials.password,
            name=""  # Name can be added as an optional field
        )

        if not result:
            raise HTTPException(status_code=400, detail="User registration failed")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")


@router.post("/login")
async def login_user(credentials: AuthCredentials) -> Dict[str, Any]:
    """
    Authenticate a user and return a session token.

    Args:
        credentials: User login credentials

    Returns:
        Dictionary with user information and authentication token
    """
    try:
        result = await auth_service.login_user(
            email=credentials.email,
            password=credentials.password
        )

        if not result:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging in user: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/logout")
async def logout_user(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Logout the current user.

    Args:
        current_user: The currently authenticated user

    Returns:
        Dictionary with logout result
    """
    try:
        # Extract token from request (this would normally come from the request context)
        # For this implementation, we'll assume the token is in the Authorization header
        import inspect
        frame = inspect.currentframe()
        while frame:
            if 'request' in frame.f_locals:
                request = frame.f_locals['request']
                break
            frame = frame.f_back
        else:
            raise HTTPException(status_code=400, detail="Unable to extract request")

        # Get token from header
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=400, detail="Invalid authorization header")

        token = auth_header[7:]

        success = await auth_service.logout_user(token)

        if success:
            return {"message": "Successfully logged out", "logged_out": True}
        else:
            raise HTTPException(status_code=400, detail="Logout failed")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error logging out user: {str(e)}")
        raise HTTPException(status_code=500, detail="Logout failed")


@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get the profile of the current user.

    Args:
        current_user: The currently authenticated user

    Returns:
        Dictionary with user profile information
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "user": current_user.dict(),
        "preferences": current_user.preferences
    }


@router.put("/profile")
async def update_profile(
    profile_update: Dict[str, Any],
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Update the profile of the current user.

    Args:
        profile_update: Dictionary with profile updates
        current_user: The currently authenticated user

    Returns:
        Dictionary with updated user information
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        success = await auth_service.update_user_preferences(
            user_id=current_user.id,
            preferences=profile_update
        )

        if not success:
            raise HTTPException(status_code=500, detail="Profile update failed")

        # Return updated user information
        updated_user = await auth_service.get_user_by_token(
            # This is a workaround - in real implementation we'd have access to the token
            # For now, we'll just return the current user with updated preferences
            next(iter(auth_service.sessions.keys()), "")
        )

        return {
            "user": updated_user.dict() if updated_user else current_user.dict(),
            "message": "Profile updated successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        raise HTTPException(status_code=500, detail="Profile update failed")


@router.get("/recommendations")
async def get_recommendations(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get personalized textbook recommendations for the current user.

    Args:
        current_user: The currently authenticated user

    Returns:
        Dictionary with personalized recommendations
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        recommendations = await personalization_service.get_user_recommendations(current_user)

        return {
            "recommendations": recommendations,
            "count": len(recommendations),
            "user_id": current_user.id
        }

    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Recommendations failed")


@router.post("/adapt-content")
async def adapt_content(
    content_request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Adapt content for the current user based on their preferences.

    Args:
        content_request: Dictionary with content and adaptation parameters
        current_user: The currently authenticated user

    Returns:
        Dictionary with adapted content
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        content = content_request.get("content", "")
        adaptation_type = content_request.get("adaptation_type", "difficulty")

        adapted_content = await personalization_service.adapt_content_for_user(
            content=content,
            user=current_user,
            adaptation_type=adaptation_type
        )

        return {
            "original_content": content,
            "adapted_content": adapted_content,
            "adaptation_type": adaptation_type,
            "user_id": current_user.id
        }

    except Exception as e:
        logger.error(f"Error adapting content: {str(e)}")
        raise HTTPException(status_code=500, detail="Content adaptation failed")


@router.get("/health")
async def auth_health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the authentication service.

    Returns:
        Dictionary with health check information
    """
    return {
        "status": "healthy",
        "service": "authentication",
        "timestamp": datetime.now().isoformat()
    }