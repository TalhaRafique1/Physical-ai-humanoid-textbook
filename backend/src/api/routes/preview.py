"""
Preview API Routes

This module defines the API endpoints for previewing textbook content.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
from datetime import datetime

from ...models.textbook import Textbook

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/content/{textbook_id}")
async def get_textbook_preview(textbook_id: str) -> Dict[str, Any]:
    """
    Get a preview of textbook content.

    Args:
        textbook_id: ID of the textbook to preview

    Returns:
        Dictionary with textbook preview information
    """
    try:
        # In a real implementation, this would query a database
        # For this demo, we'll access the in-memory storage from textbook_generation route
        from .textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Return a preview of the content (first 500 characters or full if shorter)
        preview_content = textbook.generated_content or ""
        preview_length = 500
        preview = preview_content[:preview_length] + ("..." if len(preview_content) > preview_length else "")

        return {
            "textbook_id": textbook.id,
            "title": textbook.title,
            "description": textbook.description,
            "status": textbook.status.value if hasattr(textbook.status, 'value') else textbook.status,
            "preview": preview,
            "full_content_available": len(preview_content) <= preview_length,
            "content_length": len(preview_content),
            "total_chapters": textbook.total_chapters,
            "target_audience": textbook.target_audience,
            "content_depth": textbook.content_depth,
            "writing_style": textbook.writing_style,
            "generated_at": textbook.updated_at.isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting textbook preview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting textbook preview: {str(e)}")


@router.get("/chapter/{textbook_id}/{chapter_number}")
async def get_chapter_preview(textbook_id: str, chapter_number: int) -> Dict[str, Any]:
    """
    Get a preview of a specific chapter.

    Args:
        textbook_id: ID of the textbook
        chapter_number: Number of the chapter to preview

    Returns:
        Dictionary with chapter preview information
    """
    try:
        # In a real implementation, this would query a database
        # For this demo, we'll access the in-memory storage
        from .textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # For this demo implementation, we'll extract chapter information from the content
        # In a real implementation, we would have separate chapter objects stored
        chapter_title = f"Chapter {chapter_number}: {textbook.title} - Part {chapter_number}"

        # Create a simple preview of the chapter content
        # In a real implementation, we would have actual chapter objects with content
        chapter_preview = f"This is a preview of {chapter_title}. "
        chapter_preview += f"It is part of the textbook '{textbook.title}' "
        chapter_preview += f"which is targeted at {textbook.target_audience} level audience "
        chapter_preview += f"with {textbook.content_depth} content depth."

        return {
            "textbook_id": textbook_id,
            "chapter_number": chapter_number,
            "title": chapter_title,
            "preview": chapter_preview,
            "target_audience": textbook.target_audience,
            "content_depth": textbook.content_depth
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chapter preview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting chapter preview: {str(e)}")


@router.get("/toc/{textbook_id}")
async def get_table_of_contents(textbook_id: str) -> Dict[str, Any]:
    """
    Get the table of contents for a textbook.

    Args:
        textbook_id: ID of the textbook

    Returns:
        Dictionary with table of contents information
    """
    try:
        # In a real implementation, this would query a database
        # For this demo, we'll access the in-memory storage
        from .textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        # Generate a table of contents based on the textbook information
        # In a real implementation, we would have actual chapter objects
        toc = []
        for i in range(1, textbook.total_chapters + 1):
            toc.append({
                "chapter_number": i,
                "title": f"Chapter {i}: {textbook.title} - Part {i}",
                "sections": [
                    {"section_number": f"{i}.1", "title": f"Introduction to Chapter {i}"},
                    {"section_number": f"{i}.2", "title": f"Main Concepts - Chapter {i}"},
                    {"section_number": f"{i}.3", "title": f"Summary of Chapter {i}"}
                ]
            })

        return {
            "textbook_id": textbook_id,
            "title": textbook.title,
            "total_chapters": textbook.total_chapters,
            "table_of_contents": toc
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting table of contents: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting table of contents: {str(e)}")


@router.get("/metadata/{textbook_id}")
async def get_textbook_metadata(textbook_id: str) -> Dict[str, Any]:
    """
    Get metadata for a textbook.

    Args:
        textbook_id: ID of the textbook

    Returns:
        Dictionary with textbook metadata
    """
    try:
        # In a real implementation, this would query a database
        # For this demo, we'll access the in-memory storage
        from .textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        return {
            "textbook_id": textbook.id,
            "title": textbook.title,
            "description": textbook.description,
            "status": textbook.status.value if hasattr(textbook.status, 'value') else textbook.status,
            "created_at": textbook.created_at.isoformat(),
            "updated_at": textbook.updated_at.isoformat(),
            "total_chapters": textbook.total_chapters,
            "target_audience": textbook.target_audience,
            "content_depth": textbook.content_depth,
            "writing_style": textbook.writing_style,
            "estimated_pages": textbook.estimated_pages,
            "export_formats": textbook.export_formats,
            "word_count": len((textbook.generated_content or "").split()) if textbook.generated_content else 0
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting textbook metadata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting textbook metadata: {str(e)}")