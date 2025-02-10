from pydantic import BaseModel, Field 
from typing import List 


class Feedback(BaseModel):
    """Feedback Object"""
    id: str
    rating: str
    reason: str
    query: str
    response: str