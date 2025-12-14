"""
Unit tests for the textbook generation service.

This module tests the core functionality of the textbook generation service.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from src.models.textbook import Textbook, TextbookStatus
from src.models.generation_params import GenerationParameters
from src.services.textbook_generation_service import TextbookGenerationService


@pytest.fixture
def generation_service():
    """Create an instance of TextbookGenerationService for testing."""
    service = TextbookGenerationService()
    # Mock the dependent services
    service.validation_service = AsyncMock()
    service.content_enrichment_service = AsyncMock()
    return service


@pytest.fixture
def sample_generation_params():
    """Create sample generation parameters for testing."""
    return GenerationParameters(
        id="test_params_123",
        topic="Test Topic",
        target_audience="undergraduate",
        num_chapters=2,
        content_depth="medium",
        writing_style="academic",
        sections_per_chapter=2,
        include_examples=True,
        include_exercises=False,
        required_sources=["Wikipedia"],
        excluded_topics=["test"],
        custom_instructions="Test instructions"
    )


@pytest.mark.asyncio
async def test_generate_textbook_success(generation_service, sample_generation_params):
    """Test successful textbook generation."""
    # Mock the validation service to return a successful validation
    generation_service.validation_service.validate_generation_parameters.return_value = MagicMock(
        is_valid=True
    )

    # Mock the _generate_chapters method to return some chapters
    with patch.object(generation_service, '_generate_chapters', new_callable=AsyncMock) as mock_gen_chapters:
        mock_gen_chapters.return_value = []  # Return empty list for simplicity in this test

        # Generate a textbook
        result = await generation_service.generate_textbook(sample_generation_params)

        # Verify the result
        assert result.id is not None
        assert result.title == sample_generation_params.topic
        assert result.status == TextbookStatus.COMPLETED
        assert result.total_chapters == sample_generation_params.num_chapters


@pytest.mark.asyncio
async def test_generate_textbook_with_validation_failure(generation_service, sample_generation_params):
    """Test textbook generation with validation failure."""
    # Mock the validation service to return a failed validation
    mock_validation_result = MagicMock()
    mock_validation_result.is_valid = False
    mock_validation_result.message = "Invalid parameters"
    generation_service.validation_service.validate_generation_parameters.return_value = mock_validation_result

    # Attempt to generate a textbook should raise an exception
    with pytest.raises(ValueError):
        await generation_service.generate_textbook(sample_generation_params)


@pytest.mark.asyncio
async def test_generate_chapters(generation_service, sample_generation_params):
    """Test chapter generation."""
    # Create a sample textbook
    textbook = Textbook(
        id="test_textbook_123",
        title="Test Textbook",
        description="A test textbook",
        status=TextbookStatus.GENERATING,
        target_audience="undergraduate",
        content_depth="medium",
        writing_style="academic",
        total_chapters=2
    )

    # Mock the _generate_single_chapter method
    with patch.object(generation_service, '_generate_single_chapter', new_callable=AsyncMock) as mock_gen_chapter:
        mock_chapter = MagicMock()
        mock_chapter.id = "chapter_123"
        mock_gen_chapter.return_value = mock_chapter

        # Generate chapters
        chapters = await generation_service._generate_chapters(textbook, sample_generation_params)

        # Verify that the method was called for each chapter
        assert mock_gen_chapter.call_count == sample_generation_params.num_chapters
        assert len(chapters) == sample_generation_params.num_chapters


@pytest.mark.asyncio
async def test_generate_single_chapter(generation_service, sample_generation_params):
    """Test single chapter generation."""
    # Mock the _generate_sections method
    with patch.object(generation_service, '_generate_sections', new_callable=AsyncMock) as mock_gen_sections:
        mock_gen_sections.return_value = []  # Return empty list for simplicity

        # Generate a single chapter
        chapter = await generation_service._generate_single_chapter(
            "textbook_123",
            1,
            "Test Chapter",
            sample_generation_params
        )

        # Verify the chapter was created
        assert chapter.id is not None
        assert chapter.textbook_id == "textbook_123"
        assert chapter.chapter_number == 1
        assert chapter.title == "Test Chapter"


@pytest.mark.asyncio
async def test_generate_sections(generation_service, sample_generation_params):
    """Test section generation."""
    # Mock the _generate_section_content method
    with patch.object(generation_service, '_generate_section_content', new_callable=AsyncMock) as mock_gen_content:
        mock_gen_content.return_value = "Test section content"

        # Generate sections
        sections = await generation_service._generate_sections(
            "chapter_123",
            "Test Chapter",
            sample_generation_params
        )

        # Verify the sections were created
        assert len(sections) == sample_generation_params.sections_per_chapter
        for section in sections:
            assert section.chapter_id == "chapter_123"


@pytest.mark.asyncio
async def test_generate_section_content(generation_service, sample_generation_params):
    """Test section content generation."""
    from src.models.section import ContentType

    # Generate section content
    content = await generation_service._generate_section_content(
        "Test Chapter",
        "Test Section",
        ContentType.TEXT,
        sample_generation_params
    )

    # Verify that the content includes the expected elements
    assert "Test Section" in content
    assert "Test Chapter" in content
    assert sample_generation_params.target_audience in content
    assert sample_generation_params.content_depth in content
    assert sample_generation_params.writing_style in content


@pytest.mark.asyncio
async def test_generate_learning_objectives(generation_service, sample_generation_params):
    """Test learning objectives generation."""
    objectives = await generation_service._generate_learning_objectives(
        "Test Chapter",
        sample_generation_params
    )

    # Verify that some objectives were generated
    assert len(objectives) > 0
    assert "Test Chapter" in objectives[0]


@pytest.mark.asyncio
async def test_compile_chapter_content(generation_service):
    """Test chapter content compilation."""
    from src.models.section import Section, ContentType

    # Create sample sections
    sections = [
        Section(
            id="section_1",
            chapter_id="chapter_123",
            title="Section 1",
            section_number="1.1",
            content="Content of section 1",
            content_type=ContentType.TEXT,
            word_count=10
        ),
        Section(
            id="section_2",
            chapter_id="chapter_123",
            title="Section 2",
            section_number="1.2",
            content="Content of section 2",
            content_type=ContentType.TEXT,
            word_count=15
        )
    ]

    # Compile chapter content
    content = generation_service._compile_chapter_content("Test Chapter", sections)

    # Verify the content includes chapter and section information
    assert "Test Chapter" in content
    assert "Section 1" in content
    assert "Content of section 1" in content
    assert "Section 2" in content
    assert "Content of section 2" in content


@pytest.mark.asyncio
async def test_compile_textbook_content(generation_service, sample_generation_params):
    """Test textbook content compilation."""
    # Create sample chapters
    from src.models.chapter import Chapter

    chapters = [
        Chapter(
            id="chapter_1",
            textbook_id="textbook_123",
            title="Chapter 1",
            chapter_number=1,
            content="Content of chapter 1",
            sections_count=2,
            learning_objectives=["Objective 1"]
        ),
        Chapter(
            id="chapter_2",
            textbook_id="textbook_123",
            title="Chapter 2",
            chapter_number=2,
            content="Content of chapter 2",
            sections_count=2,
            learning_objectives=["Objective 2"]
        )
    ]

    # Create a sample textbook
    textbook = Textbook(
        id="textbook_123",
        title="Test Textbook",
        description="A test textbook",
        status=TextbookStatus.COMPLETED,
        target_audience="undergraduate",
        content_depth="medium",
        writing_style="academic",
        total_chapters=2
    )

    # Compile textbook content
    content = generation_service._compile_textbook_content(textbook, chapters)

    # Verify the content includes textbook and chapter information
    assert "Test Textbook" in content
    assert "A test textbook" in content
    assert "Chapter 1" in content
    assert "Content of chapter 1" in content
    assert "Chapter 2" in content
    assert "Content of chapter 2" in content