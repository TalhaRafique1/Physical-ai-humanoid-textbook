"""
Validation Service for the textbook generation system.

This module implements functionality to validate textbook content for
coherence, educational appropriateness, and technical requirements.
"""
import asyncio
import logging
import re
from typing import Dict, Any, List, Optional
from enum import Enum


class ValidationType(Enum):
    """Enumeration of validation types."""
    CONTENT_COHERENCE = "content_coherence"
    EDUCATIONAL_APPROPRIATENESS = "educational_appropriateness"
    TECHNICAL_REQUIREMENTS = "technical_requirements"
    STRUCTURAL_INTEGRITY = "structural_integrity"


class ValidationResult:
    """Class to represent validation results."""

    def __init__(self, is_valid: bool, message: str, validation_type: ValidationType, details: Optional[Dict[str, Any]] = None):
        self.is_valid = is_valid
        self.message = message
        self.validation_type = validation_type
        self.details = details or {}


class ValidationService:
    """
    Service class for validating textbook content and structure.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.min_word_count = 50  # Minimum words per section
        self.max_word_count = 10000  # Maximum words per section
        self.min_chapter_count = 1
        self.max_chapter_count = 1000

    async def validate_textbook(self, textbook) -> List[ValidationResult]:
        """
        Validate a complete textbook for all aspects.

        Args:
            textbook: The textbook to validate

        Returns:
            List of validation results
        """
        results = []

        # Validate structural integrity
        results.append(await self.validate_structural_integrity(textbook))

        # Validate content coherence
        results.append(await self.validate_content_coherence(textbook))

        # Validate educational appropriateness
        results.append(await self.validate_educational_appropriateness(textbook))

        # Validate technical requirements
        results.append(await self.validate_technical_requirements(textbook))

        return results

    async def validate_structural_integrity(self, textbook) -> ValidationResult:
        """
        Validate the structural integrity of the textbook.

        Args:
            textbook: The textbook to validate

        Returns:
            Validation result
        """
        try:
            # Check if required fields are present
            required_fields = ['id', 'title', 'status', 'target_audience']
            missing_fields = []
            for field in required_fields:
                if not hasattr(textbook, field) or not getattr(textbook, field):
                    missing_fields.append(field)

            if missing_fields:
                return ValidationResult(
                    is_valid=False,
                    message=f"Missing required fields: {', '.join(missing_fields)}",
                    validation_type=ValidationType.STRUCTURAL_INTEGRITY,
                    details={'missing_fields': missing_fields}
                )

            # Check title length
            if not (1 <= len(textbook.title) <= 200):
                return ValidationResult(
                    is_valid=False,
                    message="Textbook title must be between 1 and 200 characters",
                    validation_type=ValidationType.STRUCTURAL_INTEGRITY,
                    details={'title_length': len(textbook.title)}
                )

            # Check chapter count
            if hasattr(textbook, 'total_chapters'):
                if not (self.min_chapter_count <= textbook.total_chapters <= self.max_chapter_count):
                    return ValidationResult(
                        is_valid=False,
                        message=f"Total chapters must be between {self.min_chapter_count} and {self.max_chapter_count}",
                        validation_type=ValidationType.STRUCTURAL_INTEGRITY,
                        details={'total_chapters': textbook.total_chapters}
                    )

            # Check target audience
            valid_audiences = ["elementary", "middle_school", "high_school", "undergraduate", "graduate", "professional", "general"]
            if hasattr(textbook, 'target_audience') and textbook.target_audience not in valid_audiences:
                return ValidationResult(
                    is_valid=False,
                    message=f"Target audience must be one of: {valid_audiences}",
                    validation_type=ValidationType.STRUCTURAL_INTEGRITY,
                    details={'target_audience': textbook.target_audience}
                )

            # Check content depth
            valid_depths = ["shallow", "medium", "deep"]
            if hasattr(textbook, 'content_depth') and textbook.content_depth not in valid_depths:
                return ValidationResult(
                    is_valid=False,
                    message=f"Content depth must be one of: {valid_depths}",
                    validation_type=ValidationType.STRUCTURAL_INTEGRITY,
                    details={'content_depth': textbook.content_depth}
                )

            # Check writing style
            valid_styles = ["formal", "conversational", "technical", "academic", "casual"]
            if hasattr(textbook, 'writing_style') and textbook.writing_style not in valid_styles:
                return ValidationResult(
                    is_valid=False,
                    message=f"Writing style must be one of: {valid_styles}",
                    validation_type=ValidationType.STRUCTURAL_INTEGRITY,
                    details={'writing_style': textbook.writing_style}
                )

            return ValidationResult(
                is_valid=True,
                message="Textbook structure is valid",
                validation_type=ValidationType.STRUCTURAL_INTEGRITY
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Error validating structural integrity: {str(e)}",
                validation_type=ValidationType.STRUCTURAL_INTEGRITY
            )

    async def validate_content_coherence(self, textbook) -> ValidationResult:
        """
        Validate the coherence of textbook content.

        Args:
            textbook: The textbook to validate

        Returns:
            Validation result
        """
        try:
            if not textbook.generated_content:
                return ValidationResult(
                    is_valid=False,
                    message="Textbook has no generated content",
                    validation_type=ValidationType.CONTENT_COHERENCE
                )

            # Check content length
            content = textbook.generated_content
            word_count = len(content.split())
            if word_count < 100:  # Minimum content length
                return ValidationResult(
                    is_valid=False,
                    message="Textbook content is too short (< 100 words)",
                    validation_type=ValidationType.CONTENT_COHERENCE,
                    details={'word_count': word_count}
                )

            # Check for basic structure (chapters, sections)
            has_chapters = '# ' in content or '## ' in content  # Markdown headers
            if not has_chapters:
                return ValidationResult(
                    is_valid=False,
                    message="Content does not appear to have proper chapter/section structure",
                    validation_type=ValidationType.CONTENT_COHERENCE
                )

            # Check for repetitive content (potential generation issue)
            paragraphs = content.split('\n\n')
            unique_paragraphs = set(paragraphs)
            repetition_ratio = 1 - (len(unique_paragraphs) / len(paragraphs)) if paragraphs else 0

            if repetition_ratio > 0.3:  # More than 30% repetition
                return ValidationResult(
                    is_valid=False,
                    message=f"High content repetition detected ({repetition_ratio:.2%})",
                    validation_type=ValidationType.CONTENT_COHERENCE,
                    details={'repetition_ratio': repetition_ratio}
                )

            return ValidationResult(
                is_valid=True,
                message="Content coherence validation passed",
                validation_type=ValidationType.CONTENT_COHERENCE,
                details={'word_count': word_count, 'has_structure': has_chapters}
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Error validating content coherence: {str(e)}",
                validation_type=ValidationType.CONTENT_COHERENCE
            )

    async def validate_educational_appropriateness(self, textbook) -> ValidationResult:
        """
        Validate the educational appropriateness of textbook content.

        Args:
            textbook: The textbook to validate

        Returns:
            Validation result
        """
        try:
            if not textbook.generated_content:
                return ValidationResult(
                    is_valid=False,
                    message="Cannot validate educational appropriateness without content",
                    validation_type=ValidationType.EDUCATIONAL_APPROPRIATENESS
                )

            content = textbook.generated_content.lower()

            # Check for inappropriate content patterns
            inappropriate_patterns = [
                r'\b(hate|violence|discrimination|profanity)\b',
                r'\b(dangerous|illegal|inappropriate)\b',
                r'\badult\b|\bnsfw\b|\bexplicit\b'
            ]

            for pattern in inappropriate_patterns:
                if re.search(pattern, content):
                    return ValidationResult(
                        is_valid=False,
                        message="Content contains potentially inappropriate material",
                        validation_type=ValidationType.EDUCATIONAL_APPROPRIATENESS,
                        details={'detected_pattern': pattern}
                    )

            # Check for educational elements based on target audience
            has_educational_elements = False
            educational_indicators = [
                'introduction', 'summary', 'exercise', 'example', 'concept', 'definition',
                'learning', 'objective', 'topic', 'chapter', 'section', 'reference'
            ]

            for indicator in educational_indicators:
                if indicator in content:
                    has_educational_elements = True
                    break

            if not has_educational_elements:
                return ValidationResult(
                    is_valid=False,
                    message="Content lacks clear educational elements",
                    validation_type=ValidationType.EDUCATIONAL_APPROPRIATENESS
                )

            # Check complexity appropriateness based on target audience
            avg_sentence_length = self._calculate_avg_sentence_length(content)
            complexity_ok = self._check_complexity_for_audience(avg_sentence_length, textbook.target_audience)

            if not complexity_ok:
                return ValidationResult(
                    is_valid=False,
                    message=f"Content complexity may not match target audience ({textbook.target_audience})",
                    validation_type=ValidationType.EDUCATIONAL_APPROPRIATENESS,
                    details={
                        'avg_sentence_length': avg_sentence_length,
                        'target_audience': textbook.target_audience
                    }
                )

            return ValidationResult(
                is_valid=True,
                message="Educational appropriateness validation passed",
                validation_type=ValidationType.EDUCATIONAL_APPROPRIATENESS,
                details={
                    'has_educational_elements': True,
                    'complexity_appropriate': True
                }
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Error validating educational appropriateness: {str(e)}",
                validation_type=ValidationType.EDUCATIONAL_APPROPRIATENESS
            )

    async def validate_technical_requirements(self, textbook) -> ValidationResult:
        """
        Validate that the textbook meets technical requirements.

        Args:
            textbook: The textbook to validate

        Returns:
            Validation result
        """
        try:
            # Check if content is too large
            content_size = len(textbook.generated_content.encode('utf-8')) if textbook.generated_content else 0
            max_size_bytes = 10 * 1024 * 1024  # 10 MB limit

            if content_size > max_size_bytes:
                return ValidationResult(
                    is_valid=False,
                    message=f"Textbook content exceeds size limit ({content_size} bytes > {max_size_bytes} bytes)",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'size_bytes': content_size, 'max_size_bytes': max_size_bytes}
                )

            # Check for proper encoding
            try:
                if textbook.generated_content:
                    textbook.generated_content.encode('utf-8').decode('utf-8')
            except UnicodeError:
                return ValidationResult(
                    is_valid=False,
                    message="Content contains invalid Unicode characters",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS
                )

            # Check for valid references/formatting
            has_valid_formatting = self._check_formatting_validity(textbook.generated_content or "")

            if not has_valid_formatting:
                return ValidationResult(
                    is_valid=False,
                    message="Content contains invalid formatting",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS
                )

            return ValidationResult(
                is_valid=True,
                message="Technical requirements validation passed",
                validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                details={'content_size': content_size}
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Error validating technical requirements: {str(e)}",
                validation_type=ValidationType.TECHNICAL_REQUIREMENTS
            )

    def _calculate_avg_sentence_length(self, content: str) -> float:
        """
        Calculate the average sentence length in the content.

        Args:
            content: The content to analyze

        Returns:
            Average sentence length in words
        """
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return 0

        total_words = 0
        for sentence in sentences:
            words = sentence.split()
            total_words += len(words)

        return total_words / len(sentences) if sentences else 0

    def _check_complexity_for_audience(self, avg_sentence_length: float, target_audience: str) -> bool:
        """
        Check if content complexity matches the target audience.

        Args:
            avg_sentence_length: Average sentence length in words
            target_audience: Target audience level

        Returns:
            True if complexity is appropriate, False otherwise
        """
        audience_complexity = {
            "elementary": (1, 8),
            "middle_school": (5, 12),
            "high_school": (8, 16),
            "undergraduate": (10, 20),
            "graduate": (12, 25),
            "professional": (12, 30),
            "general": (5, 15)
        }

        if target_audience in audience_complexity:
            min_len, max_len = audience_complexity[target_audience]
            return min_len <= avg_sentence_length <= max_len

        return True  # Default to true if audience not in mapping

    def _check_formatting_validity(self, content: str) -> bool:
        """
        Check if the content has valid formatting.

        Args:
            content: The content to check

        Returns:
            True if formatting is valid, False otherwise
        """
        # Check for balanced brackets, quotes, etc.
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}
        opening = set(pairs.keys())
        closing = set(pairs.values())

        for char in content:
            if char in opening:
                stack.append(char)
            elif char in closing:
                if not stack:
                    return False
                if pairs[stack.pop()] != char:
                    return False

        # If stack is empty, all brackets were properly closed
        return len(stack) == 0

    async def validate_generation_parameters(self, generation_params) -> ValidationResult:
        """
        Validate generation parameters before textbook generation.

        Args:
            generation_params: The generation parameters to validate

        Returns:
            Validation result
        """
        try:
            # Validate required fields
            required_fields = ['topic', 'target_audience', 'num_chapters', 'content_depth', 'writing_style']
            missing_fields = []
            for field in required_fields:
                if not hasattr(generation_params, field) or not getattr(generation_params, field):
                    missing_fields.append(field)

            if missing_fields:
                return ValidationResult(
                    is_valid=False,
                    message=f"Missing required parameters: {', '.join(missing_fields)}",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'missing_fields': missing_fields}
                )

            # Validate topic
            if not (1 <= len(generation_params.topic) <= 200):
                return ValidationResult(
                    is_valid=False,
                    message="Topic must be between 1 and 200 characters",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'topic_length': len(generation_params.topic)}
                )

            # Validate number of chapters
            if not (1 <= generation_params.num_chapters <= 100):
                return ValidationResult(
                    is_valid=False,
                    message="Number of chapters must be between 1 and 100",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'num_chapters': generation_params.num_chapters}
                )

            # Validate content depth
            valid_depths = ["shallow", "medium", "deep"]
            if generation_params.content_depth not in valid_depths:
                return ValidationResult(
                    is_valid=False,
                    message=f"Content depth must be one of: {valid_depths}",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'content_depth': generation_params.content_depth}
                )

            # Validate writing style
            valid_styles = ["formal", "conversational", "technical", "academic", "casual"]
            if generation_params.writing_style not in valid_styles:
                return ValidationResult(
                    is_valid=False,
                    message=f"Writing style must be one of: {valid_styles}",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'writing_style': generation_params.writing_style}
                )

            # Validate sections per chapter
            if not (1 <= generation_params.sections_per_chapter <= 20):
                return ValidationResult(
                    is_valid=False,
                    message="Sections per chapter must be between 1 and 20",
                    validation_type=ValidationType.TECHNICAL_REQUIREMENTS,
                    details={'sections_per_chapter': generation_params.sections_per_chapter}
                )

            return ValidationResult(
                is_valid=True,
                message="Generation parameters are valid",
                validation_type=ValidationType.TECHNICAL_REQUIREMENTS
            )

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Error validating generation parameters: {str(e)}",
                validation_type=ValidationType.TECHNICAL_REQUIREMENTS
            )


# Example usage:
# async def main():
#     from ..models.textbook import Textbook, TextbookStatus
#     textbook = Textbook(
#         id="textbook_123",
#         title="Sample Textbook",
#         description="A sample textbook for testing",
#         status=TextbookStatus.COMPLETED,
#         target_audience="undergraduate",
#         content_depth="medium",
#         writing_style="academic",
#         generated_content="# Sample Chapter\nThis is sample content for validation."
#     )
#
#     service = ValidationService()
#     results = await service.validate_textbook(textbook)
#     for result in results:
#         print(f"{result.validation_type.value}: {result.message} - Valid: {result.is_valid}")