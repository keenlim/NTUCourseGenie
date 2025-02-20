import pytest 
from unittest.mock import MagicMock, patch 
from pdf2image.exceptions import (
    PDFPopplerTimeoutError,
    PDFPageCountError,
    PDFSyntaxError,
    PDFInfoNotInstalledError
)

from course_v2.utils.academic_profiling.convert_pdf_to_image import convert_pdf_to_image

@pytest.fixture
def mock_pdf_file():
    """
    Returns a mock or sample PDF file content as bytes.
    """
    return b"%PDF-1.4 fake PDF bytes content"

def test_convert_pdf_to_image_success(mock_pdf_file):
    """
    Test that convert_pdf_to_image returns {"image": images, "status": "success"} 
    when pdf2image.convert_from_bytes is successful.
    """
    fake_images = [MagicMock(), MagicMock()]

    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes") as mock_convert_from_bytes:
        mock_convert_from_bytes.return_value = fake_images

        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "success"
        assert result["image"] == fake_images

def test_convert_pdf_to_image_not_implemented(mock_pdf_file):
    """
    Test that convert_pdf_to_image handles NotImplementedError
    and returns {"status": "error"}.
    """
    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes", side_effect=NotImplementedError):
        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "error"

def test_convert_pdf_to_image_pdf_poppler_timeout(mock_pdf_file):
    """
    Test that convert_pdf_to_image handles PDFPopplerTimeoutError
    and returns {"status": "error"}.
    """
    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes", side_effect=PDFPopplerTimeoutError):
        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "error"

def test_convert_pdf_to_image_pdf_page_count_error(mock_pdf_file):
    """
    Test that convert_pdf_to_image handles PDFPageCountError
    and returns {"status": "error"}.
    """
    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes", side_effect=PDFPageCountError):
        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "error"

def test_convert_pdf_to_image_pdf_syntax_error(mock_pdf_file):
    """
    Test that convert_pdf_to_image handles PDFSyntaxError
    and returns {"status": "error"}.
    """
    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes", side_effect=PDFSyntaxError):
        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "error"

def test_convert_pdf_to_image_pdf_info_not_installed(mock_pdf_file):
    """
    Test that convert_pdf_to_image handles PDFInfoNotInstalledError
    and returns {"status": "error"}.
    """
    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes", side_effect=PDFInfoNotInstalledError):
        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "error"

def test_convert_pdf_to_image_unknown_exception(mock_pdf_file):
    """
    Test that convert_pdf_to_image handles any other Exception
    and returns {"status": "error"}.
    """
    with patch("course_v2.utils.academic_profiling.convert_pdf_to_image.convert_from_bytes", side_effect=Exception("Unknown error")):
        result = convert_pdf_to_image(mock_pdf_file)
        assert result["status"] == "error"