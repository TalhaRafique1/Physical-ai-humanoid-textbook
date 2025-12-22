"""
RAG Chatbot API Routes

This module defines the API endpoints for the RAG chatbot functionality.
"""
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List
import logging
import asyncio
from datetime import datetime

from ....services.rag.chatbot_service import RAGChatbotService
from ....services.textbook_generation_service import TextbookGenerationService

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize services
chatbot_service = RAGChatbotService()
textbook_generation_service = TextbookGenerationService()

# In-memory storage for active chat sessions
active_chat_sessions: Dict[str, List[WebSocket]] = {}


@router.post("/query")
async def query_textbook(
    textbook_id: str,
    question: str
) -> Dict[str, Any]:
    """
    Query the textbook content using the RAG chatbot.

    Args:
        textbook_id: ID of the textbook to query
        question: The question to ask

    Returns:
        Dictionary with answer and source information
    """
    try:
        # Validate the question
        validation_result = await chatbot_service.validate_question(question)
        if not validation_result['valid']:
            raise HTTPException(status_code=400, detail=validation_result['message'])

        # Query the textbook
        result = await chatbot_service.query_textbook(textbook_id, question)

        return {
            "textbook_id": textbook_id,
            "question": question,
            "answer": result['answer'],
            "sources": result['sources'],
            "confidence": result['confidence'],
            "timestamp": datetime.now().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error querying textbook {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error querying textbook: {str(e)}")


@router.post("/index")
async def index_textbook(textbook_id: str) -> Dict[str, Any]:
    """
    Index a textbook for RAG chatbot queries.

    Args:
        textbook_id: ID of the textbook to index

    Returns:
        Dictionary with indexing result
    """
    try:
        # Get the textbook from the generation system
        from ..textbook_generation import generation_status

        if textbook_id not in generation_status:
            raise HTTPException(status_code=404, detail="Textbook not found")

        textbook_data = generation_status[textbook_id]
        textbook = textbook_data.get("textbook")

        if not textbook:
            raise HTTPException(status_code=404, detail="Textbook data not found")

        if not textbook.generated_content:
            raise HTTPException(status_code=400, detail="Textbook has no generated content to index")

        # Index the textbook
        success = await chatbot_service.index_textbook(textbook)

        if success:
            return {
                "textbook_id": textbook_id,
                "status": "indexed",
                "message": f"Successfully indexed textbook {textbook_id}",
                "chunk_count": len(chatbot_service.textbook_store[textbook_id]['chunks']) if textbook_id in chatbot_service.textbook_store else 0
            }
        else:
            raise HTTPException(status_code=500, detail=f"Failed to index textbook {textbook_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error indexing textbook {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error indexing textbook: {str(e)}")


@router.get("/info/{textbook_id}")
async def get_textbook_info(textbook_id: str) -> Dict[str, Any]:
    """
    Get information about a textbook in the RAG index.

    Args:
        textbook_id: ID of the textbook

    Returns:
        Dictionary with textbook information
    """
    try:
        info = await chatbot_service.get_textbook_info(textbook_id)

        if info is None:
            raise HTTPException(status_code=404, detail="Textbook not found in RAG index")

        return info

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting textbook info {textbook_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting textbook info: {str(e)}")


@router.get("/indexed")
async def list_indexed_textbooks() -> List[Dict[str, Any]]:
    """
    List all indexed textbooks.

    Returns:
        List of indexed textbook information
    """
    try:
        textbooks = await chatbot_service.list_indexed_textbooks()
        return textbooks

    except Exception as e:
        logger.error(f"Error listing indexed textbooks: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing indexed textbooks: {str(e)}")


@router.delete("/remove/{textbook_id}")
async def remove_textbook(textbook_id: str) -> Dict[str, Any]:
    """
    Remove a textbook from the RAG index.

    Args:
        textbook_id: ID of the textbook to remove

    Returns:
        Dictionary with removal result
    """
    try:
        success = await chatbot_service.remove_textbook(textbook_id)

        if success:
            return {
                "textbook_id": textbook_id,
                "status": "removed",
                "message": f"Successfully removed textbook {textbook_id} from RAG index"
            }
        else:
            raise HTTPException(status_code=404, detail="Textbook not found in RAG index")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing textbook {textbook_id} from RAG index: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error removing textbook: {str(e)}")


@router.websocket("/ws/chat/{textbook_id}")
async def websocket_chat(websocket: WebSocket, textbook_id: str):
    """
    WebSocket endpoint for real-time chat with the RAG chatbot.

    Args:
        websocket: WebSocket connection
        textbook_id: ID of the textbook to chat about
    """
    await websocket.accept()

    # Add websocket to active sessions for this textbook
    if textbook_id not in active_chat_sessions:
        active_chat_sessions[textbook_id] = []
    active_chat_sessions[textbook_id].append(websocket)

    try:
        # Send welcome message
        await websocket.send_json({
            "type": "welcome",
            "message": f"Connected to RAG chatbot for textbook {textbook_id}",
            "timestamp": datetime.now().isoformat()
        })

        # Chat loop
        while True:
            data = await websocket.receive_text()

            # Validate the question
            validation_result = await chatbot_service.validate_question(data)
            if not validation_result['valid']:
                await websocket.send_json({
                    "type": "error",
                    "message": validation_result['message'],
                    "timestamp": datetime.now().isoformat()
                })
                continue

            # Query the textbook
            result = await chatbot_service.query_textbook(textbook_id, data)

            # Send response
            await websocket.send_json({
                "type": "answer",
                "question": data,
                "answer": result['answer'],
                "sources": result['sources'][:2],  # Limit sources in WebSocket response
                "confidence": result['confidence'],
                "timestamp": datetime.now().isoformat()
            })

    except WebSocketDisconnect:
        # Remove websocket from active sessions
        if textbook_id in active_chat_sessions:
            active_chat_sessions[textbook_id].remove(websocket)
            if not active_chat_sessions[textbook_id]:
                del active_chat_sessions[textbook_id]
    except Exception as e:
        logger.error(f"WebSocket error for textbook {textbook_id}: {str(e)}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": "An error occurred in the chat session",
                "timestamp": datetime.now().isoformat()
            })
        except:
            pass  # Ignore if WebSocket is already closed


@router.post("/validate-question")
async def validate_question(question: str) -> Dict[str, Any]:
    """
    Validate a question before sending it to the chatbot.

    Args:
        question: The question to validate

    Returns:
        Dictionary with validation result
    """
    try:
        result = await chatbot_service.validate_question(question)
        return result
    except Exception as e:
        logger.error(f"Error validating question: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error validating question: {str(e)}")