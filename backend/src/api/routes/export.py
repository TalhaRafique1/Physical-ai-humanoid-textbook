"""
Export API Routes

This module defines the API endpoints for exporting textbooks in various formats.
"""
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import Dict, Any, List
import logging
import os
from pathlib import Path
import uuid
from datetime import datetime
import asyncio

from ...models.textbook import Textbook
from ...models.export_format import ExportFormat
from ...services.export_service import ExportService
from ...services.validation_service import ValidationService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
export_service = ExportService()
validation_service = ValidationService()


@router.post("/generate")
async def export_textbook(
    textbook_id: str = Form(...),
    format_name: str = Form(...),
    output_path: str = Form(None)
) -> Dict[str, Any]:
    """
    Export a textbook in the specified format.

    Args:
        textbook_id: ID of the textbook to export
        format_name: Name of the format to export to (PDF, DOCX, etc.)
        output_path: Optional path to save the exported file

    Returns:
        Dictionary with export result information
    """
    try:
        # For this implementation, we'll simulate having textbooks in our in-memory storage
        # In a real implementation, this would query a database
        from ..routes.textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        if textbook.status.value != "completed":
            raise HTTPException(status_code=400, detail=f"Cannot export textbook with status: {textbook.status.value}")

        # Validate the export format
        export_format = ExportFormat(
            id=f"format_{format_name.lower()}_{uuid.uuid4().hex[:8]}",
            name=format_name.upper(),
            extension=_get_extension_for_format(format_name.lower())
        )

        validation_result = await export_service.validate_export_format(export_format)
        if not validation_result['can_export']:
            raise HTTPException(
                status_code=400,
                detail=f"Export to {format_name} format is not supported: {validation_result}"
            )

        # Perform the export
        result = await export_service.export_textbook(textbook, export_format, output_path)

        if not result['success']:
            raise HTTPException(status_code=500, detail=result['message'])

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting textbook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error exporting textbook: {str(e)}")


@router.get("/formats")
async def get_supported_formats() -> List[Dict[str, Any]]:
    """
    Get a list of supported export formats.

    Returns:
        List of supported export formats
    """
    try:
        formats = await export_service.get_export_options()
        return [
            {
                "id": fmt.id,
                "name": fmt.name,
                "extension": fmt.extension,
                "description": fmt.description,
                "is_default": fmt.is_default
            }
            for fmt in formats
        ]
    except Exception as e:
        logger.error(f"Error getting export formats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting export formats: {str(e)}")


@router.get("/download/{textbook_id}/{format_name}")
async def download_exported_textbook(textbook_id: str, format_name: str):
    """
    Download an exported textbook file.

    Args:
        textbook_id: ID of the textbook to download
        format_name: Format of the exported textbook

    Returns:
        File response with the exported textbook
    """
    try:
        # For this implementation, we'll look for the exported file in the exports directory
        export_dir = Path("exports")
        safe_title = f"{textbook_id[-8:]}"  # Use last 8 chars of textbook ID
        extension = _get_extension_for_format(format_name.lower())

        # Find the file
        matching_files = list(export_dir.glob(f"*_{safe_title}{extension}"))

        if not matching_files:
            raise HTTPException(status_code=404, detail="Exported file not found")

        file_path = matching_files[0]

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Exported file not found")

        return FileResponse(
            path=file_path,
            media_type=_get_media_type_for_format(format_name.lower()),
            filename=file_path.name
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading exported textbook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error downloading exported textbook: {str(e)}")


@router.post("/validate")
async def validate_export_params(
    textbook_id: str = Form(...),
    format_name: str = Form(...)
) -> Dict[str, Any]:
    """
    Validate export parameters before starting the export process.

    Args:
        textbook_id: ID of the textbook to export
        format_name: Name of the format to export to

    Returns:
        Dictionary with validation result
    """
    try:
        # Check if textbook exists
        from ..routes.textbook_generation import generation_status

        if textbook_id not in generation_status:
            return {
                "valid": False,
                "message": "Textbook not found",
                "details": {"textbook_id": textbook_id}
            }

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            return {
                "valid": False,
                "message": "Textbook data not found",
                "details": {"textbook_id": textbook_id}
            }

        # Validate the export format
        export_format = ExportFormat(
            id=f"format_{format_name.lower()}_{uuid.uuid4().hex[:8]}",
            name=format_name.upper(),
            extension=_get_extension_for_format(format_name.lower())
        )

        validation_result = await export_service.validate_export_format(export_format)

        return {
            "valid": validation_result['can_export'],
            "format_supported": validation_result['is_supported'],
            "pandoc_available": validation_result['pandoc_available'],
            "requirements": validation_result['requirements'],
            "message": "Export parameters are valid" if validation_result['can_export'] else "Export parameters are not valid"
        }

    except Exception as e:
        logger.error(f"Error validating export parameters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error validating export parameters: {str(e)}")


def _get_extension_for_format(format_name: str) -> str:
    """
    Get the file extension for a given format name.

    Args:
        format_name: Name of the format

    Returns:
        File extension for the format
    """
    format_extensions = {
        'pdf': '.pdf',
        'docx': '.docx',
        'epub': '.epub',
        'html': '.html',
        'txt': '.txt'
    }
    return format_extensions.get(format_name.lower(), '.txt')


def _get_media_type_for_format(format_name: str) -> str:
    """
    Get the media type for a given format name.

    Args:
        format_name: Name of the format

    Returns:
        Media type for the format
    """
    format_media_types = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'epub': 'application/epub+zip',
        'html': 'text/html',
        'txt': 'text/plain'
    }
    return format_media_types.get(format_name.lower(), 'text/plain')


# In-memory storage for tracking export progress (in production, use a database)
export_status: Dict[str, Dict[str, Any]] = {}
active_export_websockets: Dict[str, List[WebSocket]] = {}


@router.get("/status/{textbook_id}")
async def get_export_status(textbook_id: str) -> Dict[str, Any]:
    """
    Get the export status for a textbook.

    Args:
        textbook_id: ID of the textbook

    Returns:
        Dictionary with export status information
    """
    try:
        # In a real implementation, this would check export job status in a database
        # For this demo, we'll return the status from our in-memory storage
        from ..routes.textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        return {
            "textbook_id": textbook_id,
            "export_formats": textbook.export_formats,
            "status": "available" if textbook.export_formats else "not_exported",
            "last_exported": textbook.updated_at.isoformat() if textbook.export_formats else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting export status: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting export status: {str(e)}")


@router.websocket("/ws/progress/{textbook_id}/{format_name}")
async def websocket_export_progress(websocket: WebSocket, textbook_id: str, format_name: str):
    """
    WebSocket endpoint for real-time progress updates during textbook export.

    Args:
        websocket: WebSocket connection
        textbook_id: ID of the textbook being exported
        format_name: Format being exported to
    """
    await websocket.accept()

    # Add websocket to active connections for this export
    export_key = f"{textbook_id}_{format_name}"
    if export_key not in active_export_websockets:
        active_export_websockets[export_key] = []
    active_export_websockets[export_key].append(websocket)

    try:
        # Send current status immediately if available
        if export_key in export_status:
            current_status = export_status[export_key]
            await websocket.send_json({
                "textbook_id": textbook_id,
                "format_name": format_name,
                "status": current_status["status"],
                "progress": current_status["progress"],
                "message": current_status["message"]
            })

        # Keep connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        # Remove websocket from active connections
        if export_key in active_export_websockets:
            active_export_websockets[export_key].remove(websocket)
            if not active_export_websockets[export_key]:
                del active_export_websockets[export_key]


async def export_progress_callback(textbook_id: str, progress: float, message: str) -> None:
    """
    Callback function to update export progress and notify connected websockets.

    Args:
        textbook_id: ID of the textbook being exported
        progress: Progress percentage (0.0 to 1.0)
        message: Status message
    """
    export_key = f"{textbook_id}_export"  # Using a generic key for any export format

    # Update in-memory status
    export_status[export_key] = {
        "status": "exporting" if progress < 1.0 else "completed",
        "progress": progress,
        "message": message,
        "updated_at": datetime.now().isoformat()
    }

    # Notify all connected websockets
    await _notify_export_websockets(textbook_id, export_status[export_key])


async def _notify_export_websockets(textbook_id: str, status_info: Dict[str, Any]):
    """
    Notify all connected websockets about export progress updates.

    Args:
        textbook_id: ID of the textbook
        status_info: Status information to send
    """
    # Check for any format-specific websocket connections
    for key in list(active_export_websockets.keys()):
        if key.startswith(textbook_id + "_"):
            disconnected = []
            for websocket in active_export_websockets[key]:
                try:
                    await websocket.send_json({
                        "textbook_id": textbook_id,
                        "format_name": key.split('_')[1],  # Extract format from key
                        "status": status_info["status"],
                        "progress": status_info["progress"],
                        "message": status_info["message"],
                        "updated_at": status_info["updated_at"]
                    })
                except WebSocketDisconnect:
                    disconnected.append(websocket)

            # Remove disconnected websockets
            for websocket in disconnected:
                if websocket in active_export_websockets[key]:
                    active_export_websockets[key].remove(websocket)