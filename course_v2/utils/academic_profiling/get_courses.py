import json
import pandas as pd
from pathlib import Path

def get_courses(DegreeKey: str, Cohort: str, Degree_Type: str, Year: int):
    """
    Get and extract courses from json files

    Attributes:
        DegreeKey (str): Degree key such as CSC, CE, DSAI etc.
        Cohort (str): Cohort year like 2021, 2022, 2023, 2024
        Degree_Type (str): Degree types such as Normal, Polytechnique, ABP, PI, PA
        Year (int): Current year of student such as 1,2,3,4,5

    Return:
        DATA (pd.DataFrame): Pandas dataframe with course information containing the following columns:
            - "Code": Course code
            - "Title": Course Title (or None if unavailable)
            - "Grades": Defaulted to None
            - "is_completed": Boolean flag indicating course completion (Default to True)
    
    Raises:
        ValueError: If the Year parameter is not a positive integer or if a JSON file contains invalid JSON
        FileNotFoundError: If any of the required JSON files are not found
        KeyError: If the specified program (combination of Cohort and Degree_Type) does not exist in the schedule data.
    """
    # Validate the Year parameter
    if not isinstance(Year, int) or Year < 1:
        raise ValueError("Year must be a postive integer.")
    
    current_dir = Path(__file__).resolve().parent
    utils_dir = current_dir.parent
    try:
        with open(f"{utils_dir}/data/courses_by_code.json", 'r') as file:
            course_info = json.load(file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file 'courses_by_code' was not found.") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"The file 'courses_by_code' contains invalid JSON.") from e

    # File: DegreeName_schedule.json (e.g. BCE_schedule.json)
    file_name = f"{DegreeKey}_schedule.json"
    try:
        with open(f"{utils_dir}/data/{file_name}", "r") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"The file '{file_name}' was not found") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"The file '{file_name}' contains invalid JSON.") from e

    if Degree_Type == 'Polytechnique':
        Degree_Type = 'Poly'
    elif Degree_Type == 'Accelerated Bachelor Programme':
        Degree_Type = 'ABP'

    program_name = f"{Cohort}_{Degree_Type}"

    if program_name not in data:
        raise KeyError(f"The program '{program_name}' was not found in the schedule data.")

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
                    "CourseType": 'C', 
                    "Year": f'Year{year}_Semester1',
                    "is_completed": True,
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
                    "CourseType": 'C', 
                    "Year": f'Year{year}_Semester2',
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
                    "CourseType": 'C', 
                    "Year": f'Year{year}_SpecialSemester',
                    "is_completed": True
                }
                courses_info.append(record)
    
    # DATA = pd.DataFrame(courses_info)

    return courses_info


