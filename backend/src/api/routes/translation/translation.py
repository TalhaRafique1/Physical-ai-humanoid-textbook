"""
Translation API Routes

This module defines the API endpoints for textbook translation functionality.
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
from datetime import datetime
import logging
import re

from ...services.translation.translation_service import TranslationService
from ...services.auth.auth_service import User, get_current_user
from ...models.textbook import Textbook
from ...models.chapter import Chapter
from ...models.section import Section

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
translation_service = TranslationService()


@router.post("/translate/{textbook_id}")
async def translate_textbook(
    textbook_id: str,
    target_language: str = "ur",
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Translate a textbook to the specified language.

    Args:
        textbook_id: ID of the textbook to translate
        target_language: Target language code (default: 'ur' for Urdu)
        current_user: The currently authenticated user

    Returns:
        Dictionary with translation result
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
        original_textbook = textbook_data.get("textbook")

        if not original_textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Validate if the language is supported
        validation_result = await translation_service.validate_translation_support(target_language)
        if not validation_result['supported']:
            raise HTTPException(
                status_code=400,
                detail=f"Translation to {target_language} is not supported. Supported languages: {validation_result['supported_languages']}"
            )

        # Perform the translation
        translated_textbook = await translation_service.translate_textbook(
            original_textbook,
            target_language
        )

        return {
            "original_textbook_id": textbook_id,
            "translated_textbook_id": translated_textbook.id,
            "target_language": target_language,
            "status": "completed",
            "message": f"Successfully translated textbook to {target_language}",
            "translated_textbook": translated_textbook.dict()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error translating textbook {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error translating textbook: {str(e)}")


@router.post("/translate/multiple/{textbook_id}")
async def translate_textbook_multiple(
    textbook_id: str,
    languages: List[str],
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Translate a textbook to multiple languages.

    Args:
        textbook_id: ID of the textbook to translate
        languages: List of target language codes
        current_user: The currently authenticated user

    Returns:
        Dictionary with translation results for each language
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
        original_textbook = textbook_data.get("textbook")

        if not original_textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Validate all languages are supported
        for lang in languages:
            validation_result = await translation_service.validate_translation_support(lang)
            if not validation_result['supported']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Translation to {lang} is not supported. Supported languages: {validation_result['supported_languages']}"
                )

        # Perform translations
        translations = await translation_service.translate_multiple_languages(
            original_textbook,
            languages
        )

        results = {}
        for lang, translated_book in translations.items():
            results[lang] = {
                "translated_textbook_id": translated_book.id,
                "status": "completed"
            }

        return {
            "original_textbook_id": textbook_id,
            "target_languages": languages,
            "status": "completed",
            "message": f"Successfully translated textbook to {len(languages)} languages",
            "results": results
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error translating textbook {textbook_id} to multiple languages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error translating textbook: {str(e)}")


@router.get("/status/{textbook_id}")
async def get_translation_status(
    textbook_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get the translation status for a textbook.

    Args:
        textbook_id: ID of the textbook
        current_user: The currently authenticated user

    Returns:
        Dictionary with translation status information
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Get translation status
        status = await translation_service.get_translation_status(textbook_id)

        return status

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting translation status for {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting translation status: {str(e)}")


@router.get("/supported-languages")
async def get_supported_languages(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Get a list of supported translation languages.

    Args:
        current_user: The currently authenticated user

    Returns:
        Dictionary with supported languages
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # For now, return the languages we have basic support for
        # In a real implementation, this would come from the translation service
        return {
            "supported_languages": [
                {"code": "ur", "name": "Urdu", "native_name": "اردو"},
                {"code": "en", "name": "English", "native_name": "English"}
            ],
            "message": "Currently supports basic translation to Urdu with more languages coming soon"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting supported languages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting supported languages: {str(e)}")


@router.post("/validate-language/{language_code}")
async def validate_language_support(
    language_code: str,
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Validate if translation to the specified language is supported.

    Args:
        language_code: The language code to validate
        current_user: The currently authenticated user

    Returns:
        Dictionary with validation result
    """
    try:
        # Verify user is authenticated
        if not current_user:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Validate language support
        result = await translation_service.validate_translation_support(language_code)

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error validating language support for {language_code}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error validating language support: {str(e)}")


@router.get("/health")
async def translation_health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the translation service.

    Returns:
        Dictionary with health check information
    """
    return {
        "status": "healthy",
        "service": "translation",
        "supported_features": ["urdu_translation", "multi_language_translation"],
        "timestamp": datetime.now().isoformat()
    }