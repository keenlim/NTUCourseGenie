import pytest
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI
from course_v2.utils.course_roadmap_utils.generate_updated_roadmap import generate_updated_roadmap  # Adjust the module name as needed
from course_v2.utils.models.roadmap import CourseData  # if needed in tests

# Define a dummy chain class that simulates the behavior of the chain returned
# by the composition of the prompt and the model.
class DummyChain:
    def __init__(self, output=None, exception=None):
        """
        If exception is set, invoke() will raise that exception.
        Otherwise, it returns the provided output.
        """
        self.output = output
        self.exception = exception

    def invoke(self, inputs):
        if self.exception is not None:
            raise self.exception
        return self.output

# Define a dummy prompt that supports the "|" operator.
# When composed with any object (e.g., the result of model.with_structured_output),
# it will simply return our dummy chain.
class DummyPrompt:
    def __or__(self, other):
        return dummy_chain  # dummy_chain will be defined in each test.

# ------------------- Test Cases -------------------

def test_generate_updated_roadmap_success(monkeypatch):
    """
    Test that generate_updated_roadmap returns a successful response with the expected output.
    """
    # Make our DummyPrompt use our dummy_chain by setting it in the global scope for this test.
    global dummy_chain  # Declare as global so DummyPrompt.__or__ can access it.
    expected_output = {"Year1_Semester1": ["Completed_Module1", "Completed_Module2"]}
    dummy_chain = DummyChain(output=expected_output)

    # Patch ChatPromptTemplate.from_messages to return a DummyPrompt instance.
    monkeypatch.setattr(ChatPromptTemplate, "from_messages", lambda messages: DummyPrompt())
    # Patch the model's with_structured_output method.
    monkeypatch.setattr(AzureChatOpenAI, "with_structured_output", lambda self, x: None)
    
    original_course_plan = [{"dummy": "plan"}]
    completed_courses = {"dummy": "completed"}
    
    result = generate_updated_roadmap(original_course_plan, completed_courses)
    
    assert result["status"] == "success"
    assert result["result"] == expected_output

def test_generate_updated_roadmap_value_error(monkeypatch):
    """
    Test that a ValueError raised in chain.invoke is caught and returns the expected error message.
    """
    global dummy_chain
    dummy_chain = DummyChain(exception=ValueError("Dummy ValueError"))

    class DummyPrompt:
        def __or__(self, other):
            return dummy_chain

    monkeypatch.setattr(ChatPromptTemplate, "from_messages", lambda messages: DummyPrompt())
    monkeypatch.setattr(AzureChatOpenAI, "with_structured_output", lambda self, x: None)

    original_course_plan = [{"dummy": "plan"}]
    completed_courses = {"dummy": "completed"}
    
    result = generate_updated_roadmap(original_course_plan, completed_courses)
    
    assert result["status"] == "error"
    assert result["message"] == "Invalid or corrupted data"

def test_generate_updated_roadmap_connection_error(monkeypatch):
    """
    Test that a ConnectionError raised in chain.invoke is caught and returns the expected error message.
    """
    global dummy_chain
    dummy_chain = DummyChain(exception=ConnectionError("Dummy ConnectionError"))

    class DummyPrompt:
        def __or__(self, other):
            return dummy_chain

    monkeypatch.setattr(ChatPromptTemplate, "from_messages", lambda messages: DummyPrompt())
    monkeypatch.setattr(AzureChatOpenAI, "with_structured_output", lambda self, x: None)

    original_course_plan = [{"dummy": "plan"}]
    completed_courses = {"dummy": "completed"}
    
    result = generate_updated_roadmap(original_course_plan, completed_courses)
    
    assert result["status"] == "error"
    assert result["message"] == "Connection Error"

def test_generate_updated_roadmap_general_exception(monkeypatch):
    """
    Test that a general Exception raised in chain.invoke is caught and returns the expected error message.
    """
    global dummy_chain
    dummy_chain = DummyChain(exception=Exception("Dummy Exception"))

    class DummyPrompt:
        def __or__(self, other):
            return dummy_chain

    monkeypatch.setattr(ChatPromptTemplate, "from_messages", lambda messages: DummyPrompt())
    monkeypatch.setattr(AzureChatOpenAI, "with_structured_output", lambda self, x: None)

    original_course_plan = [{"dummy": "plan"}]
    completed_courses = {"dummy": "completed"}
    
    result = generate_updated_roadmap(original_course_plan, completed_courses)
    
    assert result["status"] == "error"
    assert result["message"] == "Unexpected Error while generating updated course roadmap"
