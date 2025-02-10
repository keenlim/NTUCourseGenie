import json
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

class CourseData(BaseModel):
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


def generate_mermaid_timeline(course_data: CourseData, career_path) -> str:
    """
    Generates a Mermaid timeline markdown string from the course data. 
    """
    current_dir = Path(__file__).parent
    
    # We'll store each line here, then join them at the end
    lines = []
    lines.append("timeline")

    # Define a helper function to safely handle optional lists
    def format_semester(semester_name: str, courses: Optional[List[str]]) -> Optional[str]:
        """
        Returns a formatted string for the semester if courses are present,
        or None if the semester is None. 
        """
        if courses is None:
            return None
        
        return f"{semester_name}: " + " : ".join(courses)


    for year in range(1,6):
        semester1_attr = f"Year{year}_Semester1"
        semester2_attr = f"Year{year}_Semester2"
        specialSemester_attr = f"Year{year}_SpecialSemester"

        # Retrieve the list (or None)
        semester1_courses = getattr(course_data, semester1_attr, None)
        semester2_courses = getattr(course_data, semester2_attr, None)
        specialSemester_courses = getattr(course_data, specialSemester_attr, None)

        # If all are None, skip printing this year
        if semester1_courses is None and semester2_courses is None and specialSemester_courses is None: 
            continue

        # Otherwise, add a "Section Year_X" line
        lines.append(f"Section Year_{year}")

        # Format each semester line, if available 
        semester1_line = format_semester(semester1_attr, semester1_courses)
        semester2_line = format_semester(semester2_attr, semester2_courses)
        specialSemester_line = format_semester(specialSemester_attr, specialSemester_courses)

        # Append them only if they exist
        if semester1_line: 
            lines.append(f"{semester1_line}")
        if semester2_line:
            lines.append(f"{semester2_line}")
        if specialSemester_line:
            lines.append(f"{specialSemester_line}")

    # Join the lines with enwlines
    mermaid_code = "\n".join(lines)
    # Recommmend MPE Based on the career path
    # 1. Read the JSON file (list of dicts)
    with open(f"{current_dir}/data/Careers_with_key.json", 'r', encoding='utf-8') as infile:
        career_list = json.load(infile)
    
    career_info = career_list.get(career_path)

    if career_info is not None:
        electives = career_info['electives']
        mermaid_code = mermaid_code + "\n" + """Section Recommended_MPE:
        
        MPE: """ + " : ".join(electives)


    # mermaid_code = mermaid_code + "\n" + """
#     Section Recommended_MPE:
    
# MPE: SC3000 : SC4000 : SC4001 : SC4002 : SC4003 : SC4061"""

    # print(mermaid_code)
    return mermaid_code

        

