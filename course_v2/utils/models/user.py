from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import List, Optional

class LastUpdatedModel(BaseModel):
    degree: str 
    cohort: str 
    degree_key: str
    degree_type: str
    career: List[str]
    year_standing: str 
    semester: str 

    @field_validator("career")
    def career_must_not_be_empty(cls, v):
        if not v:
            raise ValueError('Career path must not be empty')

class User(BaseModel):
    """User Object"""
    id: str 
    email: str
    user: str
    last_updated: Optional[dict]
    coursedata: Optional[dict]
    career_path: Optional[str]
