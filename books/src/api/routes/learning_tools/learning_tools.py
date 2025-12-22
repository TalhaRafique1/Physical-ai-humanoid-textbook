"""
Learning Tools API Routes

This module defines the API endpoints for generating learning materials including
summaries, quizzes, and learning boosters.
"""
from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

from ....services.learning_tools.learning_tools_service import LearningToolsService
from ....services.auth.auth_service import AuthService, User
from ....models.textbook import Textbook

# Create auth service instance to get current user
auth_service = AuthService()

async def get_current_user(authorization: str = Header(None)) -> Optional[User]:
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
        user = await auth_service.get_user_by_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return user
    except Exception as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
learning_tools_service = LearningToolsService()


@router.post("/generate-summary/{textbook_id}")
async def generate_textbook_summary(
    textbook_id: str,
    length: str = "medium",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate a summary for a textbook.

    Args:
        textbook_id: ID of the textbook to summarize
        length: Length of summary ('short', 'medium', 'long')
        current_user: The currently authenticated user

    Returns:
        Dictionary with summary information
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Get the textbook from the generation system
        from ..textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Generate summary
        summary_result = await learning_tools_service.generate_textbook_summary(textbook)

        # Personalize if user has preferences
        if hasattr(current_user, 'preferences'):
            summary_result = await learning_tools_service.personalize_learning_materials(
                {"summary": summary_result},
                current_user.preferences
            )

        return {
            "textbook_id": textbook_id,
            "summary": summary_result,
            "status": "completed",
            "generated_at": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary for textbook {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")


@router.post("/generate-quiz/{textbook_id}")
async def generate_textbook_quiz(
    textbook_id: str,
    num_questions: int = 10,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate a quiz for a textbook.

    Args:
        textbook_id: ID of the textbook to generate quiz for
        num_questions: Number of questions to generate
        current_user: The currently authenticated user

    Returns:
        Dictionary with quiz information
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Get the textbook from the generation system
        from ..textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Generate quiz
        quiz_result = await learning_tools_service.generate_textbook_quiz(textbook, num_questions)

        # Personalize if user has preferences
        if hasattr(current_user, 'preferences'):
            quiz_result = await learning_tools_service.personalize_learning_materials(
                {"quiz": quiz_result},
                current_user.preferences
            )

        return {
            "textbook_id": textbook_id,
            "quiz": quiz_result,
            "status": "completed",
            "generated_at": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating quiz for textbook {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")


@router.post("/generate-learning-materials/{textbook_id}")
async def generate_learning_materials(
    textbook_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate comprehensive learning materials (summary, quiz, boosters) for a textbook.

    Args:
        textbook_id: ID of the textbook to generate materials for
        current_user: The currently authenticated user

    Returns:
        Dictionary with all learning materials
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Get the textbook from the generation system
        from ..textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Generate comprehensive learning materials
        materials = await learning_tools_service.generate_textbook_learning_materials(textbook)

        # Personalize if user has preferences
        if hasattr(current_user, 'preferences'):
            materials = await learning_tools_service.personalize_learning_materials(
                materials,
                current_user.preferences
            )

        return {
            "textbook_id": textbook_id,
            "materials": materials,
            "status": "completed",
            "generated_at": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating learning materials for textbook {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating learning materials: {str(e)}")


@router.post("/generate-chapter-materials/{textbook_id}/{chapter_number}")
async def generate_chapter_learning_materials(
    textbook_id: str,
    chapter_number: int,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Generate learning materials for a specific chapter.

    Args:
        textbook_id: ID of the textbook
        chapter_number: Chapter number to generate materials for
        current_user: The currently authenticated user

    Returns:
        Dictionary with chapter learning materials
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Get the textbook from the generation system
        from ..textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Find the specific chapter
        # In our current implementation, we don't have individual chapter access
        # So we'll use the textbook's content and generate materials for the chapter
        # For this demo, we'll just generate materials based on the textbook content
        # In a full implementation, we would have access to individual chapters

        # Create a mock chapter for the purpose of this implementation
        from ....models.chapter import Chapter
        mock_chapter = Chapter(
            id=f"mock_chapter_{chapter_number}",
            textbook_id=textbook_id,
            title=f"Chapter {chapter_number}",
            chapter_number=chapter_number,
            content=textbook.generated_content or f"Content for chapter {chapter_number}",
            sections_count=textbook.total_chapters,
            learning_objectives=[]
        )

        # Generate chapter learning materials
        materials = await learning_tools_service.generate_chapter_learning_materials(mock_chapter)

        # Personalize if user has preferences
        if hasattr(current_user, 'preferences'):
            materials = await learning_tools_service.personalize_learning_materials(
                materials,
                current_user.preferences
            )

        return {
            "textbook_id": textbook_id,
            "chapter_number": chapter_number,
            "materials": materials,
            "status": "completed",
            "generated_at": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating chapter materials for textbook {textbook_id}, chapter {chapter_number}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating chapter materials: {str(e)}")


@router.get("/health")
async def learning_tools_health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the learning tools service.

    Returns:
        Dictionary with health check information
    """
    return {
        "status": "healthy",
        "service": "learning-tools",
        "features": ["summary_generation", "quiz_generation", "learning_boosters"],
        "timestamp": datetime.now().isoformat()
    }