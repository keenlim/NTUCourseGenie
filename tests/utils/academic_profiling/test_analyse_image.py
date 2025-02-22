import pytest 
from unittest.mock import MagicMock, patch 
from course_v2.utils.academic_profiling.analyse_image import analyse_image 

@pytest.fixture 
def mock_logger():
    """
    Fixture to patch your logger.
    Ensures we capture logs and don't pollute test output.
    """
    with patch("course_v2.utils.academic_profiling.analyse_image.setup_logger") as logger_patch:
        mock_log = MagicMock()
        logger_patch.return_value = mock_log 
        yield mock_log 

@pytest.fixture
def mock_prompt():
    """
    Fixture to patch the ChatPromptTemplate. 
    We'll return a mock prompt object on which we can chain calls.
    """
    with patch("course_v2.utils.academic_profiling.analyse_image.ChatPromptTemplate.from_messages") as mock_prompt_patch:
        mock_prompt_obj = MagicMock()
        mock_prompt_patch.return_value = mock_prompt_obj
        yield mock_prompt_obj

@pytest.fixture
def mock_model():
    """
    Fixture to patch the 'model.with_structured_output(Courses)' call.
    We'll return a mock structured_llm object on which we can chain.
    """
    with patch("course_v2.utils.academic_profiling.analyse_image.model") as mock_model_patch:
        mock_model_patch.with_structured_output.return_value = MagicMock()
        yield mock_model_patch

def test_analyse_image_success(mock_logger, mock_prompt, mock_model):
    """
    Test that analyse_image runs succesfully when everything works as expected.
    """
    # Arrange
    #   - The mock_model fixture returns a mock `model`
    #   - We use `model.with_structured_output(Courses)` => a mock we'll call "structured_llm"
    structured_llm = mock_model.with_structured_output.return_value
    
    #   - Then we do prompt | structured_llm => "image_chain"
    image_chain_mock = MagicMock()
    # The "pipe" operation returns the image_chain_mock
    mock_prompt.__or__.return_value = image_chain_mock
    
    #   - Finally image_chain.invoke(...) is called
    # We want to simulate a valid result, e.g. a "Courses" object
    fake_result = MagicMock()
    image_chain_mock.invoke.return_value = fake_result

    # Act
    base64_img = "fake_base64_encoded_data"
    response = analyse_image(base64_img)

    # Assert
    # The function should return {"result": <fake_result>, "status": "success"}
    assert response["status"] == "success"
    assert response["result"] is fake_result

    # Ensure logging was used
    mock_logger.info.assert_any_call("----------- Analyse Image ----------")
    # Ensure the chain was constructed and invoked
    image_chain_mock.invoke.assert_called_once_with({"image_data": base64_img})

def test_analyse_image_value_error(mock_logger, mock_prompt, mock_model):
    """
    Test that a ValueError in the chain triggers the appropriate error response.
    """
    # Arrange
    #   - The mock_model fixture returns a mock `model`
    #   - We use `model.with_structured_output(Courses)` => a mock we'll call "structured_llm"
    structured_llm = mock_model.with_structured_output.return_value
    
    #   - Then we do prompt | structured_llm => "image_chain"
    image_chain_mock = MagicMock()
    # The "pipe" operation returns the image_chain_mock
    mock_prompt.__or__.return_value = image_chain_mock

    # Simulate chain raising a ValueError
    image_chain_mock.invoke.side_effect = ValueError("Invalid base64 data")

    # Act
    response = analyse_image("broken_base64")

    # Validate returned error structure
    assert response["status"] == "error"
    assert "message" in response
    assert "Invalid or corrupted image" in response["message"]

    # Ensure we logged the exception
    mock_logger.exception.assert_any_call("ValueError while analysing image")

def test_analyse_image_connection_error(mock_logger, mock_prompt, mock_model):
    """
    Test that a ConnectionError is caught and returns the right status & message.
    """
    # Arrange
    #   - The mock_model fixture returns a mock `model`
    #   - We use `model.with_structured_output(Courses)` => a mock we'll call "structured_llm"
    structured_llm = mock_model.with_structured_output.return_value
    
    #   - Then we do prompt | structured_llm => "image_chain"
    image_chain_mock = MagicMock()
    # The "pipe" operation returns the image_chain_mock
    mock_prompt.__or__.return_value = image_chain_mock

    # Simulate a ConnectionError
    image_chain_mock.invoke.side_effect = ConnectionError("Network down")

    # Act
    response = analyse_image("broken_base64")

    # Validate returned error structure
    assert response["status"] == "error"
    assert "message" in response
    assert "Connection Error" in response["message"]

    # Ensure we logged the exception
    mock_logger.exception.assert_any_call("ConnectionError while analysing image")

def test_analyse_image_unexpected_error(mock_logger, mock_prompt, mock_model):
    """
    Test any other generic exception is caught and a generic error returned.
    """
    # Arrange
    #   - The mock_model fixture returns a mock `model`
    #   - We use `model.with_structured_output(Courses)` => a mock we'll call "structured_llm"
    structured_llm = mock_model.with_structured_output.return_value
    
    #   - Then we do prompt | structured_llm => "image_chain"
    image_chain_mock = MagicMock()
    # The "pipe" operation returns the image_chain_mock
    mock_prompt.__or__.return_value = image_chain_mock

    # Simulate a ConnectionError
    image_chain_mock.invoke.side_effect = RuntimeError("Something unexpected")

    # Act
    response = analyse_image("some_base64")

    # Validate returned error structure
    assert response["status"] == "error"
    assert "message" in response
    assert "Error while analysing image" in response["message"]

    # Ensure we logged the exception
    mock_logger.exception.assert_any_call("Unexpected Error while analysing image")