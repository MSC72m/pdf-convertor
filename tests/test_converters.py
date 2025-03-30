import os
import tempfile
import pytest
import pytest_asyncio
import asyncio
from pathlib import Path

from file_converter import (
    PDFToDOCXConverter,
    PDFToJPGConverter,
    JPGToPDFConverter,
    HTMLToPDFConverter,
)


@pytest_asyncio.fixture
async def temp_dirs():
    """Create temporary directories for testing"""
    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        yield input_dir, output_dir


@pytest.mark.asyncio
async def test_file_manager_no_files(temp_dirs):
    """Test that the file manager handles empty directories correctly"""
    input_dir, output_dir = temp_dirs
    
    # Create a converter
    converter = PDFToDOCXConverter(input_dir, output_dir)
    
    # Try to convert files (should not raise errors)
    await converter.convert_all_files()
    
    # Check that output directory exists
    assert os.path.exists(output_dir)


@pytest.mark.asyncio
async def test_file_manager_invalid_path():
    """Test that the file manager raises an error for invalid paths"""
    with pytest.raises(FileNotFoundError):
        converter = PDFToDOCXConverter("/path/that/does/not/exist", "/tmp/output")
        await converter.convert_all_files()


@pytest.mark.asyncio
async def test_html_to_pdf_converter(temp_dirs):
    """Test HTML to PDF conversion"""
    input_dir, output_dir = temp_dirs
    
    # Create a simple HTML file
    html_content = "<html><body><h1>Test Document</h1><p>This is a test.</p></body></html>"
    html_path = os.path.join(input_dir, "test.html")
    with open(html_path, "w") as f:
        f.write(html_content)
    
    # Create converter
    converter = HTMLToPDFConverter(input_dir, output_dir)
    
    # Convert the file
    output_path = os.path.join(output_dir, "test.pdf")
    await converter._convert_single_file(html_path, output_path)
    
    # Check that the output file exists
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0 