"""
Unit tests for the validation service.

This module tests the core functionality of the validation service.
"""
import pytest
from datetime import datetime

from src.models.textbook import Textbook, TextbookStatus
from src.models.generation_params import GenerationParameters
from src.services.validation_service import ValidationService


@pytest.fixture
def validation_service():
    """Create an instance of ValidationService for testing."""
    return ValidationService()


@pytest.fixture
def sample_textbook():
    """Create a sample textbook for testing."""
    return Textbook(
        id="test_textbook_123",
        title="Test Textbook",
        description="A test textbook",
        status=TextbookStatus.COMPLETED,
        generated_content="This is test content for the textbook.",
        target_audience="undergraduate",
        content_depth="medium",
        writing_style="academic",
        total_chapters=3,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_generation_params():
    """Create sample generation parameters for testing."""
    return GenerationParameters(
        id="test_params_123",
        topic="Test Topic",
        target_audience="undergraduate",
        num_chapters=5,
        content_depth="medium",
        writing_style="academic",
        sections_per_chapter=3,
        include_examples=True,
        include_exercises=False,
        required_sources=["Wikipedia"],
        excluded_topics=["test"],
        custom_instructions="Test instructions"
    )


@pytest.mark.asyncio
async def test_validate_textbook_success(validation_service, sample_textbook):
    """Test successful validation of a textbook."""
    results = await validation_service.validate_textbook(sample_textbook)

    # Should have 4 validation results (structural integrity, content coherence, educational appropriateness, technical requirements)
    assert len(results) == 4

    # All validations should pass
    for result in results:
        assert result.is_valid is True


@pytest.mark.asyncio
async def test_validate_textbook_with_short_content(validation_service, sample_textbook):
    """Test validation of a textbook with very short content."""
    # Set content to be very short
    sample_textbook.generated_content = "Short"

    results = await validation_service.validate_textbook(sample_textbook)

    # Content coherence validation should fail
    content_coherence_result = next(
        (r for r in results if r.validation_type.value == "content_coherence"),
        None
    )
    assert content_coherence_result is not None
    assert content_coherence_result.is_valid is False


@pytest.mark.asyncio
async def test_validate_generation_parameters_success(validation_service, sample_generation_params):
    """Test successful validation of generation parameters."""
    result = await validation_service.validate_generation_parameters(sample_generation_params)

    assert result.is_valid is True


@pytest.mark.asyncio
async def test_validate_generation_parameters_missing_topic(validation_service, sample_generation_params):
    """Test validation of generation parameters with missing topic."""
    # Remove the topic
    sample_generation_params.topic = ""

    result = await validation_service.validate_generation_parameters(sample_generation_params)

    assert result.is_valid is False
    assert "Missing required parameters" in result.message


@pytest.mark.asyncio
async def test_validate_generation_parameters_invalid_chapters(validation_service, sample_generation_params):
    """Test validation of generation parameters with invalid number of chapters."""
    # Set number of chapters to an invalid value
    sample_generation_params.num_chapters = 0

    result = await validation_service.validate_generation_parameters(sample_generation_params)

    assert result.is_valid is False
    assert "Number of chapters must be between" in result.message


@pytest.mark.asyncio
async def test_validate_generation_parameters_invalid_depth(validation_service, sample_generation_params):
    """Test validation of generation parameters with invalid content depth."""
    # Set content depth to an invalid value
    sample_generation_params.content_depth = "invalid_depth"

    result = await validation_service.validate_generation_parameters(sample_generation_params)

    assert result.is_valid is False
    assert "Content depth must be one of" in result.message


@pytest.mark.asyncio
async def test_validate_generation_parameters_invalid_style(validation_service, sample_generation_params):
    """Test validation of generation parameters with invalid writing style."""
    # Set writing style to an invalid value
    sample_generation_params.writing_style = "invalid_style"

    result = await validation_service.validate_generation_parameters(sample_generation_params)

    assert result.is_valid is False
    assert "Writing style must be one of" in result.message


@pytest.mark.asyncio
async def test_validate_generation_parameters_invalid_sections(validation_service, sample_generation_params):
    """Test validation of generation parameters with invalid sections per chapter."""
    # Set sections per chapter to an invalid value
    sample_generation_params.sections_per_chapter = 0

    result = await validation_service.validate_generation_parameters(sample_generation_params)

    assert result.is_valid is False
    assert "Sections per chapter must be between" in result.message


@pytest.mark.asyncio
async def test_validate_structural_integrity_success(validation_service, sample_textbook):
    """Test successful structural integrity validation."""
    result = await validation_service.validate_structural_integrity(sample_textbook)

    assert result.is_valid is True


@pytest.mark.asyncio
async def test_validate_content_coherence_success(validation_service, sample_textbook):
    """Test successful content coherence validation."""
    result = await validation_service.validate_content_coherence(sample_textbook)

    assert result.is_valid is True


@pytest.mark.asyncio
async def test_validate_educational_appropriateness_success(validation_service, sample_textbook):
    """Test successful educational appropriateness validation."""
    result = await validation_service.validate_educational_appropriateness(sample_textbook)

    assert result.is_valid is True