import pytest
from unittest.mock import MagicMock
from course_v2.utils.academic_profiling.analyse_course_image import analyse_course_image, CourseData, AzureChatOpenAI

# Dummy output that matches the expected structure of CourseData.
dummy_course_output = {
    "Year1_Semester1": [
        "SC1003", "SC1013", "MH1810", "EG1001",
        "AB1202", "AB1301", "CC0003", "CC0005"
    ]
}

# A dummy chain that simulates the chain returned by model.with_structured_output.
class DummyChain:
    def invoke(self, params):
        # For testing, simply return the dummy output regardless of the parameters.
        return dummy_course_output

# A dummy prompt that supports the pipe operator (|).
class DummyPrompt:
    def __or__(self, other):
        # When piping with the dummy prompt, simply return the "other" (our dummy chain).
        return other

def test_analyse_course_image_success(monkeypatch):
    """
    Test that analyse_course_image returns a success dict with expected course data.
    """
    # Patch ChatPromptTemplate.from_messages to return our DummyPrompt.
    monkeypatch.setattr(
        "course_v2.utils.academic_profiling.analyse_course_image.ChatPromptTemplate.from_messages",
        lambda messages: DummyPrompt()
    )
    # Patch the AzureChatOpenAI.with_structured_output method on the class so that any instance returns DummyChain.
    monkeypatch.setattr(AzureChatOpenAI, "with_structured_output", lambda self, cls: DummyChain())

    # Define a dummy base64 image string.
    dummy_base64 = "dummy_base64_string"

    # Call the function.
    result = analyse_course_image(dummy_base64)

    # Assert that the result is a success and the output matches our dummy_course_output.
    assert result["status"] == "success"
    assert result["result"] == dummy_course_output

def test_analyse_course_image_exception(monkeypatch):
    """
    Test that analyse_course_image returns an error dict when an exception is raised.
    """
    # Force an exception by making ChatPromptTemplate.from_messages raise an error.
    monkeypatch.setattr(
        "course_v2.utils.academic_profiling.analyse_course_image.ChatPromptTemplate.from_messages",
        lambda messages: 1/0  # This will raise a ZeroDivisionError.
    )

    dummy_base64 = "dummy_base64_string"
    result = analyse_course_image(dummy_base64)

    # Assert that the function returns an error status and appropriate error message.
    assert result["status"] == "error"
    assert "Error while processing data" in result["message"]
