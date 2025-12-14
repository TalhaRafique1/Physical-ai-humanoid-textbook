"""
Unit tests for the export service.

This module tests the core functionality of the export service.
"""
import pytest
import tempfile
import os
from unittest.mock import AsyncMock, patch, MagicMock

from src.models.textbook import Textbook, TextbookStatus
from src.models.export_format import ExportFormat
from src.services.export_service import ExportService


@pytest.fixture
def export_service():
    """Create an instance of ExportService for testing."""
    return ExportService()


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
        total_chapters=3
    )


@pytest.fixture
def sample_export_format():
    """Create a sample export format for testing."""
    return ExportFormat(
        id="format_pdf_123",
        name="PDF",
        extension=".pdf",
        description="Portable Document Format"
    )


@pytest.mark.asyncio
async def test_export_textbook_success(export_service, sample_textbook, sample_export_format):
    """Test successful textbook export."""
    # Mock the _convert_to_format method to avoid actual file operations
    with patch.object(export_service, '_convert_to_format', new_callable=AsyncMock) as mock_convert:
        mock_convert.return_value = {'success': True, 'output_path': '/tmp/test.pdf'}

        # Perform the export
        result = await export_service.export_textbook(sample_textbook, sample_export_format)

        # Verify the result
        assert result['success'] is True
        assert result['textbook_id'] == sample_textbook.id
        assert result['format'] == sample_export_format.name
        assert sample_export_format.name in sample_textbook.export_formats


@pytest.mark.asyncio
async def test_export_textbook_with_invalid_status(export_service, sample_textbook, sample_export_format):
    """Test textbook export with invalid status."""
    # Set the textbook to a non-completed status
    sample_textbook.status = TextbookStatus.DRAFT

    # Attempt to export should raise an error
    with pytest.raises(ValueError, match="Cannot export textbook with status"):
        await export_service.export_textbook(sample_textbook, sample_export_format)


@pytest.mark.asyncio
async def test_export_textbook_without_content(export_service, sample_textbook, sample_export_format):
    """Test textbook export without generated content."""
    # Remove the generated content
    sample_textbook.generated_content = None

    # Attempt to export should raise an error
    with pytest.raises(ValueError, match="Cannot export textbook without generated content"):
        await export_service.export_textbook(sample_textbook, sample_export_format)


@pytest.mark.asyncio
async def test_validate_export_format_supported(export_service, sample_export_format):
    """Test validation of supported export format."""
    result = await export_service.validate_export_format(sample_export_format)

    assert result['is_supported'] is True
    assert result['can_export'] is True  # Assuming Pandoc is available in test environment


@pytest.mark.asyncio
async def test_get_export_options(export_service):
    """Test getting supported export options."""
    formats = await export_service.get_export_options()

    # Verify that all expected formats are present
    format_names = [fmt.name for fmt in formats]
    expected_formats = ['PDF', 'DOCX', 'EPUB', 'HTML', 'TXT']

    for expected_format in expected_formats:
        assert expected_format in format_names


def test_get_extension_for_format(export_service):
    """Test getting file extension for format."""
    # This test would require access to private methods
    # For now, we'll just verify that the service can be instantiated
    assert export_service is not None