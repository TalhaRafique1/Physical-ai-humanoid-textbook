"""
Textbook Generation Service for the textbook generation system.

This module implements the core logic for generating structured textbooks with chapters and sections
based on user-provided topics and parameters.
"""
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

from ..models.textbook import Textbook, TextbookStatus
from ..models.chapter import Chapter
from ..models.section import Section, ContentType
from ..models.generation_params import GenerationParameters
from .validation_service import ValidationService
from .content_enrichment_service import ContentEnrichmentService


class TextbookGenerationService:
    """
    Service class for generating textbooks with chapters and sections based on user parameters.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_service = ValidationService()
        self.content_enrichment_service = ContentEnrichmentService()

    async def generate_textbook(self,
                               generation_params: GenerationParameters,
                               progress_callback=None) -> Textbook:
        """
        Generate a complete textbook based on the provided parameters.

        Args:
            generation_params: Parameters for textbook generation
            progress_callback: Optional callback to report progress updates

        Returns:
            Generated Textbook object
        """
        self.logger.info(f"Starting textbook generation for topic: {generation_params.topic}")

        # Create initial textbook object
        textbook = Textbook(
            id=f"textbook_{uuid.uuid4().hex[:8]}",
            title=generation_params.topic,
            description=f"Textbook on {generation_params.topic}",
            target_audience=generation_params.target_audience,
            content_depth=generation_params.content_depth,
            writing_style=generation_params.writing_style,
            total_chapters=generation_params.num_chapters,
            status=TextbookStatus.GENERATING
        )

        try:
            # Update progress
            if progress_callback:
                await progress_callback(textbook.id, 0.1, "Initializing textbook structure")

            # Generate chapters
            chapters = await self._generate_chapters(textbook, generation_params, progress_callback)

            # Update textbook with generated content
            textbook.generated_content = self._compile_textbook_content(textbook, chapters)
            textbook.status = TextbookStatus.COMPLETED
            textbook.update_timestamp()

            # Update progress
            if progress_callback:
                await progress_callback(textbook.id, 1.0, "Textbook generation completed")

            self.logger.info(f"Successfully generated textbook: {textbook.id}")
            return textbook

        except Exception as e:
            self.logger.error(f"Error generating textbook: {str(e)}")
            textbook.status = TextbookStatus.FAILED
            textbook.update_timestamp()
            raise e

    async def _generate_chapters(self,
                                textbook: Textbook,
                                generation_params: GenerationParameters,
                                progress_callback=None) -> List[Chapter]:
        """
        Generate chapters for the textbook based on parameters.

        Args:
            textbook: The textbook being generated
            generation_params: Parameters for generation
            progress_callback: Optional callback to report progress updates

        Returns:
            List of generated Chapter objects
        """
        chapters = []

        for i in range(generation_params.num_chapters):
            chapter_number = i + 1
            chapter_title = await self._generate_chapter_title(textbook.title, chapter_number, generation_params)

            # Update progress
            progress = 0.1 + (0.8 * chapter_number / generation_params.num_chapters)
            if progress_callback:
                await progress_callback(textbook.id, progress, f"Generating chapter {chapter_number}")

            # Generate the chapter
            chapter = await self._generate_single_chapter(
                textbook.id,
                chapter_number,
                chapter_title,
                generation_params,
                progress_callback
            )

            chapters.append(chapter)

        return chapters

    async def _generate_single_chapter(self,
                                     textbook_id: str,
                                     chapter_number: int,
                                     chapter_title: str,
                                     generation_params: GenerationParameters,
                                     progress_callback=None) -> Chapter:
        """
        Generate a single chapter with sections.

        Args:
            textbook_id: ID of the parent textbook
            chapter_number: Number of the chapter
            chapter_title: Title of the chapter
            generation_params: Parameters for generation
            progress_callback: Optional callback to report progress updates

        Returns:
            Generated Chapter object
        """
        chapter_id = f"chapter_{uuid.uuid4().hex[:8]}"

        # Generate sections for this chapter
        sections = await self._generate_sections(
            chapter_id,
            chapter_title,
            generation_params,
            progress_callback
        )

        # Compile chapter content from sections
        chapter_content = self._compile_chapter_content(chapter_title, sections)

        # Create chapter object
        chapter = Chapter(
            id=chapter_id,
            textbook_id=textbook_id,
            title=chapter_title,
            chapter_number=chapter_number,
            content=chapter_content,
            sections_count=len(sections),
            learning_objectives=await self._generate_learning_objectives(chapter_title, generation_params)
        )

        chapter.update_content(chapter_content)

        return chapter

    async def _generate_sections(self,
                               chapter_id: str,
                               chapter_title: str,
                               generation_params: GenerationParameters,
                               progress_callback=None) -> List[Section]:
        """
        Generate sections for a chapter.

        Args:
            chapter_id: ID of the parent chapter
            chapter_title: Title of the chapter
            generation_params: Parameters for generation
            progress_callback: Optional callback to report progress updates

        Returns:
            List of generated Section objects
        """
        sections = []

        for i in range(generation_params.sections_per_chapter):
            section_number = f"{chapter_id.split('_')[1]}.{i+1}"  # Simple numbering
            section_title = await self._generate_section_title(chapter_title, i+1, generation_params)

            # Determine content type based on position
            content_type = ContentType.TEXT
            if i == 0:
                content_type = ContentType.INTRODUCTION
            elif i == generation_params.sections_per_chapter - 1:
                content_type = ContentType.CONCLUSION
            elif generation_params.include_examples and i % 2 == 0:
                content_type = ContentType.EXAMPLE
            elif generation_params.include_exercises and i % 3 == 0:
                content_type = ContentType.EXERCISE

            # Generate section content
            section_content = await self._generate_section_content(
                chapter_title,
                section_title,
                content_type,
                generation_params
            )

            # Create section object
            section = Section(
                id=f"section_{uuid.uuid4().hex[:8]}",
                chapter_id=chapter_id,
                title=section_title,
                section_number=section_number,
                content=section_content,
                content_type=content_type
            )

            section.update_content(section_content)
            sections.append(section)

        return sections

    async def _generate_chapter_title(self,
                                     textbook_topic: str,
                                     chapter_number: int,
                                     generation_params: GenerationParameters) -> str:
        """
        Generate a title for a chapter based on the textbook topic and parameters.

        Args:
            textbook_topic: Main topic of the textbook
            chapter_number: Number of the chapter
            generation_params: Parameters for generation

        Returns:
            Generated chapter title
        """
        # This is a simplified implementation - in a real system, this would use an LLM
        # to generate appropriate titles based on the topic and chapter number
        import random

        prefixes = {
            "introduction": ["Introduction to", "Basics of", "Foundations of"],
            "intermediate": ["Advanced", "Practical", "Applied"],
            "deep": ["In-depth Analysis of", "Complex Aspects of", "Specialized Topics in"]
        }

        depth_prefixes = prefixes.get(generation_params.content_depth, prefixes["introduction"])
        prefix = random.choice(depth_prefixes)

        # Generate a chapter title based on the topic
        return f"{prefix} {textbook_topic} - Chapter {chapter_number}"

    async def _generate_section_title(self,
                                     chapter_title: str,
                                     section_number: int,
                                     generation_params: GenerationParameters) -> str:
        """
        Generate a title for a section based on the chapter title and parameters.

        Args:
            chapter_title: Title of the parent chapter
            section_number: Number of the section
            generation_params: Parameters for generation

        Returns:
            Generated section title
        """
        # Simplified implementation - in reality, this would use an LLM
        import random

        section_types = {
            ContentType.INTRODUCTION: ["Overview", "Introduction", "Preliminaries"],
            ContentType.TEXT: ["Concepts", "Theory", "Fundamentals", "Principles"],
            ContentType.EXAMPLE: ["Example", "Case Study", "Illustration"],
            ContentType.EXERCISE: ["Practice", "Exercise", "Problem Set"],
            ContentType.CONCLUSION: ["Summary", "Conclusion", "Key Takeaways"]
        }

        content_type = ContentType.TEXT  # Default
        if section_number == 1:
            content_type = ContentType.INTRODUCTION
        elif section_number == generation_params.sections_per_chapter:
            content_type = ContentType.CONCLUSION
        elif generation_params.include_examples and section_number % 2 == 0:
            content_type = ContentType.EXAMPLE
        elif generation_params.include_exercises and section_number % 3 == 0:
            content_type = ContentType.EXERCISE

        possible_titles = section_types.get(content_type, section_types[ContentType.TEXT])
        base_title = random.choice(possible_titles)

        return f"{base_title} {section_number}"

    async def _generate_section_content(self,
                                      chapter_title: str,
                                      section_title: str,
                                      content_type: ContentType,
                                      generation_params: GenerationParameters) -> str:
        """
        Generate content for a section based on parameters.

        Args:
            chapter_title: Title of the parent chapter
            section_title: Title of the section
            content_type: Type of content for the section
            generation_params: Parameters for generation

        Returns:
            Generated section content
        """
        # This is a placeholder implementation - in a real system, this would use an LLM
        # to generate appropriate content based on the parameters
        base_content = f"This is the content for the section titled '{section_title}' "
        base_content += f"in the chapter '{chapter_title}'. "

        if content_type == ContentType.INTRODUCTION:
            base_content += "This section introduces the main concepts that will be covered in this chapter."
        elif content_type == ContentType.TEXT:
            base_content += "This section covers the fundamental concepts and theories related to the topic."
        elif content_type == ContentType.EXAMPLE:
            base_content += "This section provides a practical example to illustrate the concepts discussed."
        elif content_type == ContentType.EXERCISE:
            base_content += "This section contains exercises to help reinforce the learning objectives."
        elif content_type == ContentType.CONCLUSION:
            base_content += "This section summarizes the key points covered in this chapter."

        # Customize content based on target audience level
        audience_descriptors = {
            "elementary": "using simple language and basic concepts",
            "middle_school": "using age-appropriate language and examples",
            "high_school": "using appropriate academic language and concepts",
            "undergraduate": "using college-level academic language and concepts",
            "graduate": "using advanced academic language with in-depth analysis",
            "professional": "using industry-specific terminology and practical applications",
            "general": "using accessible language for general audiences"
        }
        audience_descriptor = audience_descriptors.get(generation_params.target_audience, "using appropriate language and concepts")
        base_content += f" The content is tailored for {generation_params.target_audience} level audience {audience_descriptor}."

        # Add more content based on depth and style parameters
        if generation_params.content_depth == "deep":
            base_content += " The content goes into greater detail with comprehensive explanations."
        elif generation_params.content_depth == "shallow":
            base_content += " The content provides a high-level overview of the concepts."

        if generation_params.writing_style == "formal":
            base_content += " The presentation maintains a formal academic tone."
        elif generation_params.writing_style == "conversational":
            base_content += " The presentation uses a conversational and approachable tone."
        elif generation_params.writing_style == "technical":
            base_content += " The presentation includes technical terminology and detailed analysis."

        # Apply content enrichment if sources are specified
        if generation_params.required_sources:
            base_content += f" The content incorporates information from sources: {', '.join(generation_params.required_sources)}."

        # Apply exclusions if specified
        if generation_params.excluded_topics:
            base_content += f" Note: Content related to {', '.join(generation_params.excluded_topics)} has been avoided."

        # Add custom instructions if provided
        if generation_params.custom_instructions:
            base_content += f" Additional instructions applied: {generation_params.custom_instructions}."

        return base_content

    async def _generate_learning_objectives(self,
                                          chapter_title: str,
                                          generation_params: GenerationParameters) -> List[str]:
        """
        Generate learning objectives for a chapter.

        Args:
            chapter_title: Title of the chapter
            generation_params: Parameters for generation

        Returns:
            List of learning objectives
        """
        # Simplified implementation - in reality, this would use an LLM
        objectives = [
            f"Understand the fundamental concepts of {chapter_title}",
            f"Apply the principles covered in {chapter_title} to practical scenarios",
            f"Analyze the key components discussed in {chapter_title}"
        ]

        if generation_params.content_depth == "deep":
            objectives.append(f"Evaluate advanced applications of {chapter_title}")

        return objectives

    def _compile_chapter_content(self, chapter_title: str, sections: List[Section]) -> str:
        """
        Compile chapter content from its sections.

        Args:
            chapter_title: Title of the chapter
            sections: List of sections in the chapter

        Returns:
            Compiled chapter content
        """
        content = f"# {chapter_title}\n\n"

        for section in sections:
            content += f"## {section.title}\n"
            content += f"{section.content}\n\n"

        return content

    def _compile_textbook_content(self, textbook: Textbook, chapters: List[Chapter]) -> str:
        """
        Compile textbook content from its chapters.

        Args:
            textbook: The textbook object
            chapters: List of chapters in the textbook

        Returns:
            Compiled textbook content
        """
        content = f"# {textbook.title}\n\n"
        content += f"## {textbook.description}\n\n"

        for chapter in chapters:
            content += f"## Chapter {chapter.chapter_number}: {chapter.title}\n"
            content += f"{chapter.content}\n\n"

        return content


# Example usage:
# async def main():
#     service = TextbookGenerationService()
#     params = GenerationParameters(
#         id="params_123",
#         topic="Machine Learning Fundamentals",
#         target_audience="undergraduate",
#         num_chapters=3,
#         content_depth="medium",
#         writing_style="academic",
#         sections_per_chapter=4
#     )
#
#     textbook = await service.generate_textbook(params)
#     print(f"Generated textbook: {textbook.title}")