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

class CareerFeedback(BaseModel):
    career: Literal["Blockchain Engineer", "DevOps Engineer", "Cloud Engineer/Architect", "Mixed/Virtual Reality Developer", "Cyber Security", "Software Engineer", "Full-stack Developer", "Front-End Engineer / Web Developer", "Backend Engineer", "Data Engineer", "Business Analyst", "Firmware Engineer", "Computer Hardware Engineer", "Embedded System Developer","AI Engineer", "Machine Learning Engineer", "Data Scientist", "Data Analyst", "AI Scientist", "System Architect", "Cybersecurity Consultant/Analyst", "Product Manager", "Entrepreneur", "Quantitative Analyst/Developer"] = Field(
        description="Career recommendation based on the courses and grades."
    )
    explanation: str = Field(description="Provide a detailed explanation of why you recommend the career")
    strength: str = Field(description = "Short description of the strength of the student")
    weakness: str = Field(description="Short description of the weakness of the student")