from pydantic import BaseModel 
from typing import Optional, List

class CourseData(BaseModel):
    Year1_Semester1: List[str]
    Year1_Semester2: List[str]
    Year1_SpecialSemester: Optional[List[str]]
    Year2_Semester1:List[str]
    Year2_Semester2: List[str]
    Year3_Semester1: List[str]
    Year3_Semester2: List[str]
    Year4_Semester1: List[str]
    Year4_Semester2: Optional[List[str]]
    Year5_Semester1: Optional[List[str]]
    Year5_Semester2: Optional[List[str]]
    Year3_SpecialSemester: Optional[List[str]]


class MermaidCourseData(BaseModel):
    Year1_Semester1: Optional[List[str]]
    Year1_Semester2: Optional[List[str]]
    Year1_SpecialSemester: Optional[List[str]]
    Year2_Semester1: Optional[List[str]]
    Year2_Semester2: Optional[List[str]]
    Year3_Semester1: Optional[List[str]]
    Year3_Semester2: Optional[List[str]]
    Year4_Semester1: Optional[List[str]]
    Year4_Semester2: Optional[List[str]]
    Year5_Semester1: Optional[List[str]]
    Year5_Semester2: Optional[List[str]]
    Year3_SpecialSemester: Optional[List[str]]