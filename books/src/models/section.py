"""
Section model for the textbook generation system.

This module defines the Section entity based on the data model specification.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from enum import Enum


class ContentType(str, Enum):
    """Enumeration of possible content types for sections."""
    TEXT = "text"
    EXAMPLE = "example"
    EXERCISE = "exercise"
    SUMMARY = "summary"
    INTRODUCTION = "introduction"
    CONCLUSION = "conclusion"


class Section(BaseModel):
    """
    Section entity - A subdivision of a chapter containing specific topics or concepts.
    """
    id: str = Field(..., description="Unique identifier for the section")
    chapter_id: str = Field(..., description="Reference to the parent chapter")
    title: str = Field(..., min_length=1, max_length=100, description="Title of the section")
    section_number: str = Field(..., description="Number of the section (e.g., '1.1', '1.2')")
    content: Optional[str] = Field(default="", description="The section content")
    content_type: ContentType = Field(default=ContentType.TEXT, description="Type of content")
    word_count: int = Field(default=0, ge=0, description="Number of words in the section")

    @validator('title')
    def validate_title(cls, v):
        if not (1 <= len(v) <= 100):
            raise ValueError('Title must be between 1 and 100 characters')
        return v

    @validator('section_number')
    def validate_section_number(cls, v):
        # Basic validation for section number format (e.g., "1.1", "2.3.1")
        import re
        # Allow formats like "1", "1.1", "1.2.3", etc.
        pattern = r'^\d+(\.\d+)*$'
        if not re.match(pattern, v):
            raise ValueError('Section number must follow proper hierarchy format (e.g., "1.1", "1.2.3")')
        return v

    @validator('word_count')
    def validate_word_count(cls, v):
        if v < 0:
            raise ValueError('Word count must be non-negative')
        return v

    def update_content(self, new_content: str):
        """Update the section content and adjust word count."""
        self.content = new_content
        self.word_count = len(new_content.split()) if new_content else 0

    def set_content_type(self, content_type: ContentType):
        """Set the content type of the section."""
        self.content_type = content_type


# Example usage:
# section = Section(
#     id="section_123",
#     chapter_id="chapter_123",
#     title="What is Artificial Intelligence?",
#     section_number="1.1",
#     content="Artificial Intelligence (AI) is intelligence demonstrated by machines...",
#     content_type=ContentType.TEXT,
#     word_count=150
# )