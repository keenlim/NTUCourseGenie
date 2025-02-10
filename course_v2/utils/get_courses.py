import json
import pandas as pd
from pathlib import Path

def get_courses(DegreeKey: str, Cohort: str, Degree_Type: str, Year: int):
    """
    DegreeKey: CSC, CE, DSAI etc.
    Cohort: 2021, 2022, 2023, 2024
    Degree_Type: Normal, Polytechnique, ABP, PI, PA
    Year: 1,2,3,4,5

    RETURN
    DATA = pd.DataFrame(
    [
        {"Code": "SC1003", "Title": "Introduction to Computational Thinking", "Grades": "A", "is_completed": True}
    ]
    """
    current_dir = Path(__file__).parent
    with open(f"{current_dir}/data/courses_by_code.json", 'r') as file:
        course_info = json.load(file)

    # File: DegreeName_schedule.json (e.g. BCE_schedule.json)
    file_name = f"{DegreeKey}_schedule.json"
    with open(f"{current_dir}/data/{file_name}", "r") as f:
        data = json.load(f)

    if Degree_Type == 'Polytechnique':
        Degree_Type = 'Poly'
    elif Degree_Type == 'Accelerated Bachelor Programme':
        Degree_Type = 'ABP'

    program_name = f"{Cohort}_{Degree_Type}"

    course_data = data[program_name]

    courses_info = []

    for year in range(1,Year+1):
        semester1_attr = f"Year{year}_Semester1"
        semester2_attr = f"Year{year}_Semester2"
        specialSemester_attr = f"Year{year}_SpecialSemester"

        # Retrieve the list (or None)
        semester1_courses = course_data.get(semester1_attr, None)
        semester2_courses = course_data.get(semester2_attr, None)
        specialSemester_courses = course_data.get(specialSemester_attr, None)

        # If all are None, skip 
        if semester1_courses is None and semester2_courses is None and specialSemester_courses is None:
            continue

        # Otherwise, format them into a dictionary
        if semester1_courses:
            for code in semester1_courses:
                course = course_info.get(code)
                course_title = course["title"] if course else None
                record = {
                    "Code": code, 
                    "Title": course_title, 
                    "Grades" : None, 
                    "is_completed": True
                }
                courses_info.append(record)
        if semester2_courses:
            for code in semester2_courses:
                course = course_info.get(code)
                course_title = course["title"] if course else None
                record = {
                    "Code": code, 
                    "Title": course_title, 
                    "Grades" : None, 
                    "is_completed": True
                }
                courses_info.append(record)
        
        if specialSemester_courses:
            for code in specialSemester_courses:
                course = course_info.get(code)
                course_title = course["title"] if course else None
                record = {
                    "Code": code, 
                    "Title": course_title, 
                    "Grades" : None, 
                    "is_completed": True
                }
                courses_info.append(record)
    
    DATA = pd.DataFrame(courses_info)

    # print(courses_info)

    return DATA


