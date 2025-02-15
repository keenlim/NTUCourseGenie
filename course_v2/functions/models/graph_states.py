import operator
from typing_extensions import TypedDict, List
from typing import Annotated, Sequence
from pydantic import BaseModel
from langgraph.graph.message import add_messages

class InputState(TypedDict):
    query: str
    cached_messages: Annotated[Sequence[BaseModel], operator.add]
    user_profile: dict

class OverallState(TypedDict):
    messages: Annotated[Sequence[BaseModel], add_messages]
    query: Annotated[Sequence[BaseModel], operator.add]
    next_action: str
    cypher_statement: str 
    cypher_errors: List[str]
    database_records: List[dict]
    steps: Annotated[List[str], operator.add]
    entity: Annotated[Sequence[BaseModel], operator.add]
    cached_messages: Annotated[Sequence[BaseModel], operator.add]
    user_profile: dict

class OutputState(TypedDict):
    answer: str 
    steps: List[str]
    cypher_statement: str
    database_records: List[dict]