"""
Textbook model for the textbook generation system.

This module defines the Textbook entity based on the data model specification.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field, validator


class TextbookStatus(str, Enum):
    """Enumeration of possible textbook statuses."""
    DRAFT = "draft"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPORTED = "exported"


class Textbook(BaseModel):
    """
    Textbook entity - A structured educational document containing chapters, sections, and metadata.
    """
    id: str = Field(..., description="Unique identifier for the textbook")
    title: str = Field(..., min_length=1, max_length=200, description="Title of the textbook")
    description: str = Field(default="", description="Brief description of the textbook content")
    created_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the textbook was created")
    updated_at: datetime = Field(default_factory=datetime.now, description="Timestamp when the textbook was last modified")
    status: TextbookStatus = Field(default=TextbookStatus.DRAFT, description="Current status of the textbook")
    total_chapters: int = Field(default=0, ge=0, le=1000, description="Number of chapters in the textbook")
    target_audience: str = Field(..., description="Intended audience level (e.g., high school, undergraduate, graduate)")
    content_depth: str = Field(..., description="Depth level (shallow, medium, deep)")
    writing_style: str = Field(..., description="Writing style preference (formal, conversational, technical)")
    estimated_pages: int = Field(default=0, ge=0, description="Estimated number of pages")
    generated_content: Optional[str] = Field(default=None, description="The actual textbook content in structured format")
    export_formats: List[str] = Field(default=[], description="List of supported export formats")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata (author, subject, tags, etc.)")

    @validator('title')
    def validate_title(cls, v):
        if not (1 <= len(v) <= 200):
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @validator('total_chapters')
    def validate_total_chapters(cls, v):
        if not (0 <= v <= 1000):
            raise ValueError('Total chapters must be between 0 and 1000')
        return v

    @validator('target_audience')
    def validate_target_audience(cls, v):
        valid_audiences = ["elementary", "middle_school", "high_school", "undergraduate", "graduate", "professional", "general"]
        if v not in valid_audiences:
            raise ValueError(f'Target audience must be one of: {valid_audiences}')
        return v

    @validator('content_depth')
    def validate_content_depth(cls, v):
        valid_depths = ["shallow", "medium", "deep"]
        if v not in valid_depths:
            raise ValueError(f'Content depth must be one of: {valid_depths}')
        return v

    @validator('writing_style')
    def validate_writing_style(cls, v):
        valid_styles = ["formal", "conversational", "technical", "academic", "casual"]
        if v not in valid_styles:
            raise ValueError(f'Writing style must be one of: {valid_styles}')
        return v

    def update_timestamp(self):
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.now()

    def add_export_format(self, format_name: str):
        """Add a new export format to the textbook."""
        if format_name not in self.export_formats:
            self.export_formats.append(format_name)
            self.update_timestamp()

    def set_status(self, status: TextbookStatus):
        """Set the status of the textbook and update the timestamp."""
        self.status = status
        self.update_timestamp()


# Example usage:
# textbook = Textbook(
#     id="textbook_123",
#     title="Introduction to AI",
#     description="A comprehensive textbook on artificial intelligence",
#     target_audience="undergraduate",
#     content_depth="medium",
#     writing_style="academic",
#     total_chapters=5
# )