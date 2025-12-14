"""
GenerationParameters model for the textbook generation system.

This module defines the GenerationParameters entity based on the data model specification.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class GenerationParameters(BaseModel):
    """
    GenerationParameters entity - User-specified settings for textbook generation.
    """
    id: str = Field(..., description="Unique identifier for the parameters set")
    user_id: Optional[str] = Field(default=None, description="Reference to the user who created these parameters (optional)")
    topic: str = Field(..., min_length=1, max_length=200, description="Main topic or subject area for the textbook")
    target_audience: str = Field(..., description="Intended audience level")
    num_chapters: int = Field(..., ge=1, le=100, description="Desired number of chapters")
    content_depth: str = Field(..., description="Depth level preference")
    writing_style: str = Field(..., description="Writing style preference")
    sections_per_chapter: int = Field(default=3, ge=1, le=20, description="Desired number of sections per chapter")
    include_examples: bool = Field(default=True, description="Whether to include examples")
    include_exercises: bool = Field(default=False, description="Whether to include exercises")
    required_sources: List[str] = Field(default=[], description="List of required source materials to reference")
    excluded_topics: List[str] = Field(default=[], description="List of topics to avoid")
    custom_instructions: Optional[str] = Field(default="", description="Any special instructions for generation")

    @validator('topic')
    def validate_topic(cls, v):
        if not (1 <= len(v) <= 200):
            raise ValueError('Topic must be between 1 and 200 characters')
        return v

    @validator('target_audience')
    def validate_target_audience(cls, v):
        valid_audiences = ["elementary", "middle_school", "high_school", "undergraduate", "graduate", "professional", "general"]
        if v not in valid_audiences:
            raise ValueError(f'Target audience must be one of: {valid_audiences}')
        return v

    @validator('num_chapters')
    def validate_num_chapters(cls, v):
        if not (1 <= v <= 100):
            raise ValueError('Number of chapters must be between 1 and 100')
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

    @validator('sections_per_chapter')
    def validate_sections_per_chapter(cls, v):
        if not (1 <= v <= 20):
            raise ValueError('Sections per chapter must be between 1 and 20')
        return v

    def add_required_source(self, source: str):
        """Add a required source to the list."""
        if source not in self.required_sources:
            self.required_sources.append(source)

    def add_excluded_topic(self, topic: str):
        """Add an excluded topic to the list."""
        if topic not in self.excluded_topics:
            self.excluded_topics.append(topic)

    def update_custom_instructions(self, instructions: str):
        """Update the custom instructions."""
        self.custom_instructions = instructions


# Example usage:
# params = GenerationParameters(
#     id="params_123",
#     topic="Machine Learning Fundamentals",
#     target_audience="undergraduate",
#     num_chapters=5,
#     content_depth="medium",
#     writing_style="academic",
#     sections_per_chapter=4,
#     include_examples=True,
#     include_exercises=True,
#     required_sources=["Wikipedia", "arXiv"],
#     excluded_topics=["advanced mathematics", "proprietary algorithms"]
# )