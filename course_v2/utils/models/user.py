from pydantic import BaseModel, Field
from typing import List, Optional

class User(BaseModel):
    """User Object"""
    id: str 
    email: str
    user: str
    last_updated: Optional[dict]
    coursedata: Optional[dict]
    career_path: Optional[str]