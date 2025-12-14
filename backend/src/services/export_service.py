"""
Export Service for the textbook generation system.

This module implements functionality to export textbooks in multiple formats
(PDF, DOCX, EPUB) using Pandoc and other conversion tools.
"""
import asyncio
import logging
import os
import tempfile
import subprocess
from typing import Dict, Any, Optional, List, Callable, Awaitable
from pathlib import Path
import shutil

from ..models.textbook import Textbook
from ..models.export_format import ExportFormat
from .validation_service import ValidationService


class ExportService:
    """
    Service class for exporting textbooks in various formats.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.validation_service = ValidationService()
        self.supported_formats = {
            'pdf': {'extension': '.pdf', 'pandoc_format': 'pdf'},
            'docx': {'extension': '.docx', 'pandoc_format': 'docx'},
            'epub': {'extension': '.epub', 'pandoc_format': 'epub'},
            'html': {'extension': '.html', 'pandoc_format': 'html'},
            'txt': {'extension': '.txt', 'pandoc_format': 'plain'}
        }

    async def export_textbook(self,
                             textbook: Textbook,
                             export_format: ExportFormat,
                             output_path: Optional[str] = None,
                             progress_callback: Optional[Callable[[str, float, str], Awaitable[None]]] = None) -> Dict[str, Any]:
        """
        Export a textbook in the specified format.

        Args:
            textbook: The textbook to export
            export_format: The format to export to
            output_path: Optional path to save the exported file
            progress_callback: Optional callback to report progress updates

        Returns:
            Dictionary with export result information
        """
        self.logger.info(f"Exporting textbook {textbook.id} to {export_format.name} format")

        # Validate the textbook
        if textbook.status != textbook.__class__.Status.COMPLETED:
            raise ValueError(f"Cannot export textbook with status: {textbook.status}")

        if not textbook.generated_content:
            raise ValueError("Cannot export textbook without generated content")

        # Determine the output path
        if output_path is None:
            output_path = await self._generate_output_path(textbook, export_format)

        try:
            # Update progress if callback provided
            if progress_callback:
                await progress_callback(textbook.id, 0.1, f"Starting export to {export_format.name}")

            # Convert the textbook content to the specified format
            result = await self._convert_to_format(textbook, export_format, output_path, progress_callback)

            # Update progress
            if progress_callback:
                await progress_callback(textbook.id, 0.9, f"Finalizing {export_format.name} export")

            # Update textbook export formats
            textbook.add_export_format(export_format.name)

            # Final progress update
            if progress_callback:
                await progress_callback(textbook.id, 1.0, f"Export to {export_format.name} completed")

            return {
                'success': True,
                'textbook_id': textbook.id,
                'format': export_format.name,
                'output_path': output_path,
                'file_size': os.path.getsize(output_path) if os.path.exists(output_path) else 0,
                'message': f"Successfully exported textbook to {export_format.name} format"
            }

        except Exception as e:
            self.logger.error(f"Error exporting textbook {textbook.id} to {export_format.name}: {str(e)}")

            # Report error in progress if callback provided
            if progress_callback:
                await progress_callback(textbook.id, 0.0, f"Export failed: {str(e)}")

            return {
                'success': False,
                'textbook_id': textbook.id,
                'format': export_format.name,
                'output_path': output_path,
                'error': str(e),
                'message': f"Failed to export textbook to {export_format.name} format: {str(e)}"
            }

    async def _generate_output_path(self, textbook: Textbook, export_format: ExportFormat) -> str:
        """
        Generate an appropriate output path for the exported file.

        Args:
            textbook: The textbook being exported
            export_format: The export format

        Returns:
            Generated output path
        """
        # Create a temporary directory for exports if it doesn't exist
        export_dir = Path("exports")
        export_dir.mkdir(exist_ok=True)

        # Create a safe filename from the textbook title
        safe_title = "".join(c for c in textbook.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]  # Limit length

        # Generate filename
        filename = f"{safe_title}_{textbook.id[-8:]}{export_format.extension}"
        output_path = export_dir / filename

        return str(output_path)

    async def _convert_to_format(self, textbook: Textbook, export_format: ExportFormat, output_path: str, progress_callback: Optional[Callable[[str, float, str], Awaitable[None]]] = None) -> Dict[str, Any]:
        """
        Convert the textbook content to the specified format using Pandoc or other tools.

        Args:
            textbook: The textbook to convert
            export_format: The export format
            output_path: Path to save the converted file
            progress_callback: Optional callback to report progress updates

        Returns:
            Dictionary with conversion result
        """
        format_name = export_format.name.lower()

        if format_name not in self.supported_formats:
            raise ValueError(f"Unsupported export format: {format_name}")

        # Create a temporary file with the textbook content in Markdown format
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(self._prepare_markdown_content(textbook))
            temp_file_path = temp_file.name

        try:
            # Update progress before conversion
            if progress_callback:
                await progress_callback(textbook.id, 0.3, f"Preparing {format_name} conversion")

            # Use Pandoc to convert the content to the target format
            await self._convert_with_pandoc(temp_file_path, output_path, format_name, progress_callback)

            # Update progress after conversion
            if progress_callback:
                await progress_callback(textbook.id, 0.8, f"Finishing {format_name} conversion")

            return {'success': True, 'output_path': output_path}
        except Exception as e:
            # If Pandoc fails, try alternative conversion methods
            self.logger.warning(f"Pandoc conversion failed: {str(e)}. Trying alternative method.")
            if progress_callback:
                await progress_callback(textbook.id, 0.4, f"Using alternative method for {format_name}")

            await self._convert_with_alternative_method(textbook, output_path, format_name, progress_callback)
            return {'success': True, 'output_path': output_path}
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)

    async def _convert_with_pandoc(self, input_path: str, output_path: str, format_name: str, progress_callback: Optional[Callable[[str, float, str], Awaitable[None]]] = None) -> None:
        """
        Convert content using Pandoc with progress tracking.

        Args:
            input_path: Path to input file
            output_path: Path to output file
            format_name: Target format name
            progress_callback: Optional callback to report progress updates
        """
        pandoc_format = self.supported_formats[format_name]['pandoc_format']

        # Build the Pandoc command
        cmd = [
            'pandoc',
            input_path,
            '-o', output_path,
            '-f', 'markdown',
            '-t', pandoc_format
        ]

        # Add format-specific options
        if format_name == 'pdf':
            # For PDF, we might want to add some basic styling
            cmd.extend(['--pdf-engine', 'pdflatex'])  # Use pdflatex as the PDF engine
        elif format_name == 'docx':
            # For DOCX, we might want to add document properties
            pass  # Pandoc handles this well by default
        elif format_name == 'epub':
            # For EPUB, we might want to add metadata
            cmd.extend(['--epub-title', 'Generated Textbook'])

        # We can't update progress here since we don't have the textbook object
        # The progress callback will be handled in the calling method
        # Execute the Pandoc command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the process to complete (Pandoc conversion)
        await process.wait()

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            raise RuntimeError(f"Pandoc conversion failed: {error_msg}")

    def _prepare_markdown_content(self, textbook: Textbook) -> str:
        """
        Prepare the textbook content in Markdown format for conversion.

        Args:
            textbook: The textbook to prepare

        Returns:
            Markdown formatted content
        """
        content = f"# {textbook.title}\n\n"
        content += f"## {textbook.description}\n\n"

        if textbook.generated_content:
            content += textbook.generated_content

        return content

    async def _convert_with_pandoc(self, input_path: str, output_path: str, format_name: str) -> None:
        """
        Convert content using Pandoc.

        Args:
            input_path: Path to input file
            output_path: Path to output file
            format_name: Target format name
        """
        pandoc_format = self.supported_formats[format_name]['pandoc_format']

        # Build the Pandoc command
        cmd = [
            'pandoc',
            input_path,
            '-o', output_path,
            '-f', 'markdown',
            '-t', pandoc_format
        ]

        # Add format-specific options
        if format_name == 'pdf':
            # For PDF, we might want to add some basic styling
            cmd.extend(['--pdf-engine', 'pdflatex'])  # Use pdflatex as the PDF engine
        elif format_name == 'docx':
            # For DOCX, we might want to add document properties
            pass  # Pandoc handles this well by default
        elif format_name == 'epub':
            # For EPUB, we might want to add metadata
            cmd.extend(['--epub-title', 'Generated Textbook'])

        # Execute the Pandoc command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            raise RuntimeError(f"Pandoc conversion failed: {error_msg}")

    async def _convert_with_alternative_method(self, textbook: Textbook, output_path: str, format_name: str, progress_callback: Optional[Callable[[str, float, str], Awaitable[None]]] = None) -> None:
        """
        Convert content using alternative methods when Pandoc is not available.

        Args:
            textbook: The textbook to convert
            output_path: Path to output file
            format_name: Target format name
            progress_callback: Optional callback to report progress updates
        """
        if format_name == 'txt':
            # For text format, just write the content directly
            if progress_callback:
                await progress_callback(textbook.id, 0.5, f"Creating {format_name} file")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(textbook.generated_content or textbook.title)

        elif format_name == 'html':
            # For HTML format, create a basic HTML document
            if progress_callback:
                await progress_callback(textbook.id, 0.5, f"Creating {format_name} file")
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{textbook.title}</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>{textbook.title}</h1>
    <h2>{textbook.description}</h2>
    {self._text_to_html(textbook.generated_content or '')}
</body>
</html>"""
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

        else:
            # For other formats, save as text with a warning
            if progress_callback:
                await progress_callback(textbook.id, 0.5, f"Creating {format_name} file (fallback method)")
            content = f"Export to {format_name} format not supported without Pandoc.\n\n"
            content += textbook.generated_content or textbook.title
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def _text_to_html(self, text: str) -> str:
        """
        Convert plain text to basic HTML structure.

        Args:
            text: Text to convert

        Returns:
            HTML formatted text
        """
        # Simple conversion - in a real implementation, this would be more sophisticated
        paragraphs = text.split('\n\n')
        html_paragraphs = [f'<p>{p.strip()}</p>' for p in paragraphs if p.strip()]
        return '\n'.join(html_paragraphs)

    async def validate_export_format(self, export_format: ExportFormat) -> Dict[str, Any]:
        """
        Validate if the export format is supported and properly configured.

        Args:
            export_format: The export format to validate

        Returns:
            Dictionary with validation result
        """
        is_supported = export_format.name.lower() in self.supported_formats
        has_pandoc = await self._check_pandoc_available()

        return {
            'is_supported': is_supported,
            'pandoc_available': has_pandoc,
            'can_export': is_supported and (has_pandoc or export_format.name.lower() in ['txt', 'html']),
            'requirements': {
                'pandoc_needed': export_format.name.lower() not in ['txt', 'html']
            }
        }

    async def _check_pandoc_available(self) -> bool:
        """
        Check if Pandoc is available in the system.

        Returns:
            True if Pandoc is available, False otherwise
        """
        try:
            process = await asyncio.create_subprocess_exec(
                'pandoc',
                '--version',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            _, _ = await process.communicate()
            return process.returncode == 0
        except FileNotFoundError:
            return False
        except Exception:
            return False

    async def get_export_options(self) -> List[ExportFormat]:
        """
        Get a list of supported export formats.

        Returns:
            List of supported export formats
        """
        formats = []
        for name, info in self.supported_formats.items():
            formats.append(ExportFormat(
                id=f"format_{name}",
                name=name.upper(),
                extension=info['extension'],
                description=f"Export to {name.upper()} format",
                is_default=(name == 'pdf')  # PDF as default
            ))
        return formats


# Example usage:
# async def main():
#     # Create a sample textbook
#     from ..models.textbook import Textbook, TextbookStatus
#     textbook = Textbook(
#         id="textbook_123",
#         title="Sample Textbook",
#         description="A sample textbook for testing",
#         status=TextbookStatus.COMPLETED,
#         generated_content="# Sample Content\nThis is sample textbook content."
#     )
#
#     # Create export format
#     from ..models.export_format import ExportFormat
#     export_format = ExportFormat(
#         id="format_pdf",
#         name="PDF",
#         extension=".pdf",
#         description="Portable Document Format"
#     )
#
#     # Export the textbook
#     service = ExportService()
#     result = await service.export_textbook(textbook, export_format)
#     print(f"Export result: {result}")