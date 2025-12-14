"""
ExportFormat model for the textbook generation system.

This module defines the ExportFormat entity based on the data model specification.
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class ExportFormat(BaseModel):
    """
    ExportFormat entity - Specification for export format options.
    """
    id: str = Field(..., description="Unique identifier for the format")
    name: str = Field(..., description="Format name (PDF, DOCX, EPUB, etc.)")
    extension: str = Field(..., description="File extension")
    description: str = Field(default="", description="Description of the format")
    options: Dict[str, Any] = Field(default={}, description="Format-specific options (margins, fonts, etc.)")
    is_default: bool = Field(default=False, description="Whether this is the default export format")

    @validator('name')
    def validate_name(cls, v):
        valid_formats = ["PDF", "DOCX", "EPUB", "HTML", "TXT", "ODT", "RTF"]
        if v.upper() not in [fmt.upper() for fmt in valid_formats]:
            raise ValueError(f'Format name must be one of: {valid_formats}')
        return v

    @validator('extension')
    def validate_extension(cls, v):
        valid_extensions = [".pdf", ".docx", ".epub", ".html", ".txt", ".odt", ".rtf"]
        if v.lower() not in valid_extensions:
            raise ValueError(f'Extension must be one of: {valid_extensions}')
        return v

    def set_option(self, key: str, value: Any):
        """Set a format-specific option."""
        self.options[key] = value

    def get_option(self, key: str, default: Any = None) -> Any:
        """Get a format-specific option."""
        return self.options.get(key, default)

    def is_supported_format(self) -> bool:
        """Check if this is a supported export format."""
        valid_formats = ["PDF", "DOCX", "EPUB", "HTML", "TXT", "ODT", "RTF"]
        return self.name.upper() in [fmt.upper() for fmt in valid_formats]


# Example usage:
# pdf_format = ExportFormat(
#     id="format_pdf_123",
#     name="PDF",
#     extension=".pdf",
#     description="Portable Document Format",
#     options={"margins": "1in", "font_size": 12},
#     is_default=True
# )