from functions.models.graph_states import OverallState
from typing import Literal

def guardrails_condition(
    state: OverallState
) -> Literal["entity_identifier", "generate_final_answer"]:
    if state.get("next_action") == "end":
        return "generate_final_answer"
    elif state.get("next_action") == "courses":
        return "entity_identifier"

def validate_cypher_condition(
    state: OverallState, 
) -> Literal["generate_final_answer", "correct_cypher", "execute_cypher"]:
    if state.get("next_action") == "end":
        return "generate_final_answer"
    elif state.get("next_action") == "correct_cypher":
        return "correct_cypher"
    elif state.get("next_action") == "execute_cypher":
        return "execute_cypher"