import builtins
import json
import pytest
from io import StringIO

# Import the functions and classes from your module.
# Replace "your_module" with the actual module name where app_response and Retrieval_Workflow are defined.
from course_v2.functions.app import app_response, Retrieval_Workflow

# --- Dummy Classes & Functions for Testing ---

class DummyWorkflow:
    def stream(self, input_data, config):
        # Yield a dummy response that mimics one step of the workflow
        yield {"dummy": "value", "generate_final_answer": {"answer": "dummy answer"}}
        # Yield a final dummy message containing "__end__" to stop further processing
        yield {"__end__": True}

class DummyStatus:
    def __init__(self, label, expanded):
        self.label = label
        self.expanded = expanded

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def update(self, label, state, expanded):
        self.label = label

def dummy_workflow_function(self):
    # Instead of building the full workflow graph, return our dummy workflow instance
    return DummyWorkflow()

# Dummy function that raises an exception to simulate a failure in workflow_function
def raise_exception_workflow(self):
    raise Exception("Forced Exception")

# --- Pytest Fixtures to Patch External Dependencies ---

@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    # Patch streamlit's status context manager with our DummyStatus
    import streamlit as st
    monkeypatch.setattr(st, "status", lambda label, expanded: DummyStatus(label, expanded))
    
    # Patch Retrieval_Workflow.workflow_function to return our DummyWorkflow instance
    monkeypatch.setattr(Retrieval_Workflow, "workflow_function", dummy_workflow_function)
    
    # Patch open so that when agents_explanation.json is read, it returns a dummy JSON
    original_open = builtins.open

    def dummy_open(file, mode='r', *args, **kwargs):
        if "agents_explanation.json" in file:
            # Provide a minimal JSON content for agent explanations
            return StringIO(json.dumps({"dummy": "dummy explanation"}))
        return original_open(file, mode, *args, **kwargs)
    
    monkeypatch.setattr(builtins, "open", dummy_open)

    # Patch CallbackHandler (from langfuse.callback) to do nothing on initialization.
    # Adjust the import path as needed if CallbackHandler is imported differently.
    from langfuse.callback import CallbackHandler
    monkeypatch.setattr(CallbackHandler, "__init__", lambda self, **kwargs: None)

# --- Unit Test for app_response ---

def test_app_response():
    # Define dummy inputs
    query = "test query"
    chat_id = "12345"
    cached_messages = []
    user_profile = {"name": "test user"}
    user_id = "user123"
    
    # Call the function under test
    result = app_response(query, chat_id, cached_messages, user_profile, user_id)
    
    # Assertions: we expect a successful response with "dummy answer" from our dummy workflow
    assert result["status"] == "success"
    assert result["response"] == "dummy answer"
    assert "run_id" in result

def test_app_response_handles_exception(monkeypatch):
    # Monkeypatch the workflow_function method to always raise an exception
    monkeypatch.setattr(Retrieval_Workflow, "workflow_function", raise_exception_workflow)
    
    # Dummy inputs
    query = "test query"
    chat_id = "test_chat_id"
    cached_messages = []
    user_profile = {"name": "test user"}
    user_id = "test_user"
    
    # Call the function, expecting it to catch the exception and return an error dict
    result = app_response(query, chat_id, cached_messages, user_profile, user_id)
    
    # Assertions: status must be "error", error message contains "Unexpected Error", and run_id exists.
    assert result["status"] == "error"
    assert "Unexpected Error" in result["message"]
    assert "run_id" in result
