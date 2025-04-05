from typing import List, Literal, Optional 
from pydantic import BaseModel, Field

class Search(BaseModel):
    """Search over a database of courses and degree records"""
    queries: List[str] = Field(
        ...,
        description="Distinct queries to search for"
    )
    program: Literal["COURSE", "DEGREE"] = Field(
        ...,
        description="Program to look things up for. Should be `COURSE` or `DEGREE`"
    )

class SearchList(BaseModel):
    searchList: List[Search]

class UpdateQuery(BaseModel):
    updatedQuery: str 

# GraphRAG 
class Property(BaseModel):
    """
    Represents a filter condition based on a specific node property in a graph in a Cypher statement. 
    """
    node_label: str = Field(
        description="The label of the node to which this property belongs."
    )
    property_key: str = Field(description="The key of the property being filtered.")
    property_value: str = Field(
        description="The value that the property is being matched against."
    )

class ValidateCypherOutput(BaseModel):
    """
    Represents the validation result of a Cypher query's output, including any errors and applied filters.
    """
    errors: Optional[List[str]] = Field(
        description="A list of syntax or semantical errors in the Cypher statement. Always explain the discrepancy between schema and Cypher statement"
    )
    filters: Optional[List[Property]] = Field(
        description="A list of property-based filters applied in the Cypher statement."
    )

# Guardrails Agent
class GuardrailsOutput(BaseModel):
    decision: Literal["courses", "end"] = Field(
        description="Decision on whether the question is related to courses or degrees offered in College of Computing and Data Science"
    )

class History_Query(BaseModel):
    """Rewritten query to better align with the user's chat history"""
    rewritten_query: str

class ValidateOutput(BaseModel):
    results: Literal["relevant", "irrelevant"] = Field(
        description="Decision on whether the database records is relevant or irrelevant to the query."
    )