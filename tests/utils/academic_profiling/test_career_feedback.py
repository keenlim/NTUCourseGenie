import pytest
from unittest.mock import MagicMock
from course_v2.utils.academic_profiling.feedback_career import career_feedback, CareerFeedback, AzureChatOpenAI  # Replace "your_module" with your actual module path.

# Dummy output matching CareerFeedback fields
dummy_output = {
    "career": "Data Scientist",
    "explanation": "You have strong analytical skills and a solid background in statistics.",
    "strength": "Excellent at problem solving",
    "weakness": "Limited real-world project experience"
}

class DummyChain:
    def invoke(self, params):
        # In a real scenario, you might verify the incoming params
        return dummy_output

class DummyPrompt:
    # This dummy prompt should support the pipe operator (|) and return a chain.
    def __or__(self, other):
        return other  # For testing, we simply return the "other" (which will be our dummy chain)


def test_career_feedback_success(monkeypatch):
    """
    Test that career_feedback returns the expected dummy output when all dependencies work.
    """
    # Patch ChatPromptTemplate.from_messages to return our dummy prompt.
    monkeypatch.setattr(
        "course_v2.utils.academic_profiling.feedback_career.ChatPromptTemplate.from_messages",
        lambda messages: DummyPrompt()
    )

    # Patch model.with_structured_output so that it returns our dummy chain.
    monkeypatch.setattr(AzureChatOpenAI, "with_structured_output", lambda self, cls: DummyChain())

    # Define some dummy inputs.
    degree = "Computer Science"
    career_interest = "Software Engineer"
    courses_taken = [{"course": "CS101", "grade": "A"}]

    # Call the function.
    result = career_feedback(degree, career_interest, courses_taken)

    # Check that the returned output matches our dummy output.
    assert result == dummy_output
    # Also, you can assert that the output conforms to the CareerFeedback model, e.g.:
    validated = CareerFeedback(**result)
    assert validated.career == dummy_output["career"]

def test_career_feedback_exception(monkeypatch):
    """
    Test that career_feedback returns None when an exception is raised.
    """
    # Force an exception by making ChatPromptTemplate.from_messages raise an error.
    monkeypatch.setattr(
        "course_v2.utils.academic_profiling.feedback_career.ChatPromptTemplate.from_messages",
        lambda messages: 1/0  # This will raise ZeroDivisionError
    )

    degree = "Computer Science"
    career_interest = "Software Engineer"
    courses_taken = [{"course": "CS101", "grade": "A"}]

    result = career_feedback(degree, career_interest, courses_taken)
    assert result is None
