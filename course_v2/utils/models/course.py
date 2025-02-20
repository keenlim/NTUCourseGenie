from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class CourseImage(BaseModel):
    Code: str = Field(description="Specific Course Code of each course, for example 'SC1005'")
    Title: str = Field(description="Specific Course Title of each course, for example 'Digital Logic'")
    Grades: str = Field(description="Grades extracted from each course, for example 'A'")
    is_Completed: bool = Field(description="By default will be True")

class Courses(BaseModel):
    Course: List[CourseImage]

class CourseInfo(BaseModel):
    courseCode: str = Field(description="Specific course code")
    courseType: Literal['C', 'P', 'BDE'] = Field(description="Course Type, C suggests Core, P suggests MPE, BDE suggests BDE courses")

class CourseData(BaseModel):
    Year1_Semester1: Optional[List[CourseInfo]]
    Year1_Semester2: Optional[List[CourseInfo]]
    Year1_SpecialSemester: Optional[List[CourseInfo]]
    Year2_Semester1: Optional[List[CourseInfo]]
    Year2_Semester2: Optional[List[CourseInfo]]
    Year3_Semester1: Optional[List[CourseInfo]]
    Year3_Semester2: Optional[List[CourseInfo]]
    Year4_Semester1: Optional[List[CourseInfo]]
    Year4_Semester2: Optional[List[CourseInfo]]
    Year5_Semester1: Optional[List[CourseInfo]]
    Year5_Semester2: Optional[List[CourseInfo]]
    Year3_SpecialSemester: Optional[List[CourseInfo]]