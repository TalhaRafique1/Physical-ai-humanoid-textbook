"""
Chapter model for the textbook generation system.

This module defines the Chapter entity based on the data model specification.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from .textbook import Textbook


class Chapter(BaseModel):
    """
    Chapter entity - A major division of a textbook containing sections and content.
    """
    id: str = Field(..., description="Unique identifier for the chapter")
    textbook_id: str = Field(..., description="Reference to the parent textbook")
    title: str = Field(..., min_length=1, max_length=100, description="Title of the chapter")
    chapter_number: int = Field(..., ge=1, description="Sequential number of the chapter")
    word_count: int = Field(default=0, ge=0, description="Number of words in the chapter")
    sections_count: int = Field(default=0, ge=0, description="Number of sections in the chapter")
    content: Optional[str] = Field(default="", description="The chapter content")
    summary: Optional[str] = Field(default="", description="Brief summary of the chapter")
    learning_objectives: List[str] = Field(default=[], description="List of learning objectives for this chapter")

    @validator('title')
    def validate_title(cls, v):
        if not (1 <= len(v) <= 100):
            raise ValueError('Title must be between 1 and 100 characters')
        return v

    @validator('chapter_number')
    def validate_chapter_number(cls, v):
        if v <= 0:
            raise ValueError('Chapter number must be positive')
        return v

    @validator('word_count')
    def validate_word_count(cls, v):
        if v < 0:
            raise ValueError('Word count must be non-negative')
        return v

    @validator('sections_count')
    def validate_sections_count(cls, v):
        if v < 0:
            raise ValueError('Sections count must be non-negative')
        return v

    def update_content(self, new_content: str):
        """Update the chapter content and adjust word count."""
        self.content = new_content
        self.word_count = len(new_content.split()) if new_content else 0

    def add_learning_objective(self, objective: str):
        """Add a learning objective to the chapter."""
        if objective not in self.learning_objectives:
            self.learning_objectives.append(objective)

    def set_sections_count(self, count: int):
        """Set the number of sections in the chapter."""
        if count >= 0:
            self.sections_count = count
        else:
            raise ValueError("Sections count must be non-negative")


# Example usage:
# chapter = Chapter(
#     id="chapter_123",
#     textbook_id="textbook_123",
#     title="Introduction to AI",
#     chapter_number=1,
#     content="This chapter introduces the fundamentals of artificial intelligence...",
#     summary="An overview of AI concepts and applications",
#     learning_objectives=["Define artificial intelligence", "Identify key AI techniques"]
# )