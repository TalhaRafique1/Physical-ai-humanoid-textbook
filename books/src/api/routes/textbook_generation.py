"""
Textbook Generation API Routes

This module defines the API endpoints for textbook generation functionality.
"""
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from typing import Dict, Any, List
import asyncio
import logging
import uuid
from datetime import datetime

from ...models.generation_params import GenerationParameters
from ...models.textbook import Textbook, TextbookStatus
from ...services.textbook_generation_service import TextbookGenerationService
from ...services.validation_service import ValidationService

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory storage for tracking generation progress (in production, use a database)
generation_status: Dict[str, Dict[str, Any]] = {}
active_websockets: Dict[str, List[WebSocket]] = {}

# Initialize services
generation_service = TextbookGenerationService()
validation_service = ValidationService()


@router.post("/generate")
async def generate_textbook(params: GenerationParameters) -> Dict[str, Any]:
    """
    Generate a new textbook based on the provided parameters.

    Args:
        params: Generation parameters including topic, audience, etc.

    Returns:
        Dictionary with textbook generation information
    """
    try:
        # Validate the generation parameters
        validation_result = await validation_service.validate_generation_parameters(params)
        if not validation_result.is_valid:
            raise HTTPException(status_code=400, detail=validation_result.message)

        # Create a new textbook object
        textbook = Textbook(
            id=f"textbook_{uuid.uuid4().hex[:8]}",
            title=params.topic,
            description=f"Textbook on {params.topic}",
            target_audience=params.target_audience,
            content_depth=params.content_depth,
            writing_style=params.writing_style,
            total_chapters=params.num_chapters,
            status=TextbookStatus.GENERATING
        )

        # Store initial status
        generation_status[textbook.id] = {
            "status": "generating",
            "progress": 0.0,
            "message": "Initialization started",
            "textbook": textbook,
            "updated_at": datetime.now()
        }

        # Start generation in background
        # Note: In a real implementation, you would use a proper task queue like Celery
        # For this demo, we'll simulate by starting a background task
        asyncio.create_task(_simulate_generation(textbook.id, params))

        return {
            "textbook_id": textbook.id,
            "status": "started",
            "message": "Textbook generation started",
            "estimated_completion": "Calculating..."
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting textbook generation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error starting textbook generation: {str(e)}")


@router.get("/status/{textbook_id}")
async def get_generation_status(textbook_id: str) -> Dict[str, Any]:
    """
    Get the current status of a textbook generation process.

    Args:
        textbook_id: ID of the textbook being generated

    Returns:
        Dictionary with generation status information
    """
    if textbook_id not in generation_status:
        raise HTTPException(status_code=404, detail="Textbook generation not found")

    status_info = generation_status[textbook_id]
    return {
        "textbook_id": textbook_id,
        "status": status_info["status"],
        "progress": status_info["progress"],
        "message": status_info["message"],
        "updated_at": status_info["updated_at"].isoformat()
    }


@router.get("/list")
async def list_textbooks() -> List[Dict[str, Any]]:
    """
    List all textbooks in the system.

    Returns:
        List of textbook information
    """
    try:
        # In a real implementation, this would query a database
        # For this demo, we'll return textbooks from our in-memory storage
        textbooks = []
        for textbook_id, status_info in generation_status.items():
            textbook = status_info.get("textbook")
            if textbook:
                textbooks.append({
                    "id": textbook.id,
                    "title": textbook.title,
                    "status": textbook.status.value if hasattr(textbook.status, 'value') else textbook.status,
                    "created_at": textbook.created_at.isoformat(),
                    "updated_at": textbook.updated_at.isoformat(),
                    "total_chapters": textbook.total_chapters,
                    "target_audience": textbook.target_audience
                })

        # Sort by creation date (most recent first)
        textbooks.sort(key=lambda x: x["created_at"], reverse=True)

        return textbooks
    except Exception as e:
        logger.error(f"Error listing textbooks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing textbooks: {str(e)}")


@router.get("/{textbook_id}")
async def get_textbook(textbook_id: str) -> Dict[str, Any]:
    """
    Get details of a specific textbook.

    Args:
        textbook_id: ID of the textbook to retrieve

    Returns:
        Textbook information
    """
    if textbook_id not in generation_status:
        raise HTTPException(status_code=404, detail="Textbook not found")

    status_info = generation_status[textbook_id]
    textbook = status_info.get("textbook")

    if not textbook:
        raise HTTPException(status_code=404, detail="Textbook data not found")

    return {
        "id": textbook.id,
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
        "export_formats": textbook.export_formats
    }


@router.websocket("/ws/progress/{textbook_id}")
async def websocket_progress(websocket: WebSocket, textbook_id: str):
    """
    WebSocket endpoint for real-time progress updates during textbook generation.

    Args:
        websocket: WebSocket connection
        textbook_id: ID of the textbook to track
    """
    await websocket.accept()

    # Add websocket to active connections for this textbook
    if textbook_id not in active_websockets:
        active_websockets[textbook_id] = []
    active_websockets[textbook_id].append(websocket)

    try:
        # Send current status immediately
        if textbook_id in generation_status:
            current_status = generation_status[textbook_id]
            await websocket.send_json({
                "textbook_id": textbook_id,
                "status": current_status["status"],
                "progress": current_status["progress"],
                "message": current_status["message"]
            })

        # Keep connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Remove websocket from active connections
        if textbook_id in active_websockets:
            active_websockets[textbook_id].remove(websocket)
            if not active_websockets[textbook_id]:
                del active_websockets[textbook_id]


async def _simulate_generation(textbook_id: str, params: GenerationParameters):
    """
    Simulate the textbook generation process (in a real implementation, this would be the actual generation).

    Args:
        textbook_id: ID of the textbook being generated
        params: Generation parameters
    """
    try:
        # Update status to indicate generation is in progress
        generation_status[textbook_id].update({
            "status": "generating",
            "progress": 0.1,
            "message": "Starting generation process",
            "updated_at": datetime.now()
        })

        # Notify all connected websockets
        await _notify_websockets(textbook_id, generation_status[textbook_id])

        # In a real implementation, we would call the generation service here
        # For this demo, we'll simulate the process
        textbook = generation_status[textbook_id]["textbook"]

        # Update progress
        generation_status[textbook_id].update({
            "progress": 0.3,
            "message": "Analyzing topic and creating outline",
            "updated_at": datetime.now()
        })
        await _notify_websockets(textbook_id, generation_status[textbook_id])
        await asyncio.sleep(1)  # Simulate processing time

        generation_status[textbook_id].update({
            "progress": 0.6,
            "message": "Generating chapter content",
            "updated_at": datetime.now()
        })
        await _notify_websockets(textbook_id, generation_status[textbook_id])
        await asyncio.sleep(2)  # Simulate processing time

        generation_status[textbook_id].update({
            "progress": 0.9,
            "message": "Finalizing textbook structure",
            "updated_at": datetime.now()
        })
        await _notify_websockets(textbook_id, generation_status[textbook_id])
        await asyncio.sleep(1)  # Simulate processing time

        # Complete the generation
        textbook.status = TextbookStatus.COMPLETED
        textbook.generated_content = f"This is the generated content for {textbook.title}. It contains {textbook.total_chapters} chapters with detailed information."
        textbook.update_timestamp()

        generation_status[textbook_id].update({
            "status": "completed",
            "progress": 1.0,
            "message": "Textbook generation completed successfully",
            "updated_at": datetime.now()
        })
        await _notify_websockets(textbook_id, generation_status[textbook_id])

    except Exception as e:
        logger.error(f"Error in textbook generation simulation: {str(e)}")
        generation_status[textbook_id].update({
            "status": "failed",
            "progress": 0.0,
            "message": f"Generation failed: {str(e)}",
            "updated_at": datetime.now()
        })
        await _notify_websockets(textbook_id, generation_status[textbook_id])


async def _notify_websockets(textbook_id: str, status_info: Dict[str, Any]):
    """
    Notify all connected websockets about status updates.

    Args:
        textbook_id: ID of the textbook
        status_info: Status information to send
    """
    if textbook_id in active_websockets:
        disconnected = []
        for websocket in active_websockets[textbook_id]:
            try:
                await websocket.send_json({
                    "textbook_id": textbook_id,
                    "status": status_info["status"],
                    "progress": status_info["progress"],
                    "message": status_info["message"],
                    "updated_at": status_info["updated_at"].isoformat()
                })
            except WebSocketDisconnect:
                disconnected.append(websocket)

        # Remove disconnected websockets
        for websocket in disconnected:
            if websocket in active_websockets[textbook_id]:
                active_websockets[textbook_id].remove(websocket)