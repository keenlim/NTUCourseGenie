import pytest
from unittest.mock import patch, MagicMock
from course_v2.utils.academic_profiling.process_files import process_files  # Update to correct import path

@pytest.fixture
def mock_uploaded_pdf():
    """
    Returns a mock file object simulating a PDF upload.
    """
    mock_file = MagicMock()
    mock_file.name = "fake.pdf"
    mock_file.getvalue.return_value = b"PDF_FILE_BYTES"
    return mock_file

@pytest.fixture
def mock_uploaded_image():
    """
    Returns a mock file object simulating an image upload.
    """
    mock_file = MagicMock()
    mock_file.name = "photo.jpg"
    mock_file.getvalue.return_value = b"IMAGE_FILE_BYTES"
    return mock_file

def test_process_files_pdf_success(mock_uploaded_pdf):
    """
    Test a successful PDF workflow:
    - convert_pdf_to_image returns success with a list of images
    - analyse_image returns a dict with "status": "success" and a Pydantic-like "result".
    """
    # Mock return values from convert_pdf_to_image and analyse_image
    mock_images = {
        "status": "success",
        "image": [MagicMock()]  # one PIL Image mock
    }

    # Simulate a pydantic-like object for .dict(by_alias=True)
    mock_pydantic_obj = MagicMock()
    mock_pydantic_obj.dict.return_value = {"Course": ["CSC101", "MTH202"]}

    # analyse_image returns a dict: {"status": "success", "result": mock_pydantic_obj}
    mock_analysis_result = {
        "status": "success",
        "result": mock_pydantic_obj
    }

    with patch("course_v2.utils.academic_profiling.process_files.convert_pdf_to_image", return_value=mock_images):
        with patch("course_v2.utils.academic_profiling.process_files.analyse_image", return_value=mock_analysis_result):
            # Call process_files with one PDF
            result = process_files([mock_uploaded_pdf])

    assert result["status"] == "success"
    assert result["message"] == "Successfully analysed the uploaded files"
    assert "CSC101" in result["courseData"]
    assert "MTH202" in result["courseData"]
    # imageData should contain the base64 string
    assert len(result["imageData"]) == 1

def test_process_files_pdf_convert_error(mock_uploaded_pdf):
    """
    Test that if convert_pdf_to_image returns an error,
    the function returns an error response immediately.
    """
    mock_images = {
        "status": "error"
    }

    with patch("course_v2.utils.academic_profiling.process_files.convert_pdf_to_image", return_value=mock_images):
        result = process_files([mock_uploaded_pdf])

    assert result["status"] == "error"
    assert result["message"] == "Error analysing PDF"
    assert result["courseData"] == []
    assert result["imageData"] == []

def test_process_files_pdf_analysis_error(mock_uploaded_pdf):
    """
    Test that if analyse_image returns "status": "error",
    the function returns an error response immediately.
    """
    mock_images = {
        "status": "success",
        "image": [MagicMock()]
    }
    mock_analysis_result = {
        "status": "error",
        "message": "Unexpected Error from model"
    }

    with patch("course_v2.utils.academic_profiling.process_files.convert_pdf_to_image", return_value=mock_images):
        with patch("course_v2.utils.academic_profiling.process_files.analyse_image", return_value=mock_analysis_result):
            result = process_files([mock_uploaded_pdf])

    assert result["status"] == "error"
    assert result["message"] == "Unexpected Error"
    assert result["courseData"] == []
    assert result["imageData"] == []

def test_process_files_pdf_analysis_exception(mock_uploaded_pdf):
    """
    Test that if an exception is raised while analyzing a PDF,
    the function returns an error response with "Unable to analyse transcript".
    """
    mock_images = {
        "status": "success",
        "image": [MagicMock()]
    }

    with patch("course_v2.utils.academic_profiling.process_files.convert_pdf_to_image", return_value=mock_images):
        with patch("course_v2.utils.academic_profiling.process_files.analyse_image", side_effect=Exception("Some error")):
            result = process_files([mock_uploaded_pdf])

    assert result["status"] == "error"
    assert "Unable to analyse transcript" in result["message"]
    assert result["courseData"] == []
    assert result["imageData"] == []

def test_process_files_non_pdf_success(mock_uploaded_image):
    """
    Test a non-PDF (e.g., .jpg) scenario, which calls analyse_image directly
    and returns success if there's no error.
    """
    # If it's not PDF, the code just base64-encodes
    # and calls analyse_image(encoded).dict(by_alias=True)
    # We'll mock 'analyse_image' to return a pydantic-like dict
    mock_analyze_return = MagicMock()
    mock_analyze_return.dict.return_value = {"Course": ["CSC101", "MTH202"]}

    mock_analysis_result = {
        "status": "success",
        "result": mock_analyze_return
    }

    with patch("course_v2.utils.academic_profiling.process_files.analyse_image", return_value=mock_analysis_result):
        result = process_files([mock_uploaded_image])

    assert result["status"] == "success"
    assert "Successfully analysed the uploaded files" in result["message"]
    assert "CSC101" in result["courseData"]
    assert len(result["imageData"]) == 1

def test_process_files_non_pdf_exception(mock_uploaded_image):
    """
    Test that if an exception is raised during the analysis of a non-PDF,
    the function returns an error response with 'Unable to analyse transcript'.
    """
    with patch("course_v2.utils.academic_profiling.process_files.analyse_image", side_effect=Exception("Some error")):
        result = process_files([mock_uploaded_image])

    assert result["status"] == "error"
    assert "Unable to analyse transcript" in result["message"]
    assert result["courseData"] == []
    assert result["imageData"] == []
