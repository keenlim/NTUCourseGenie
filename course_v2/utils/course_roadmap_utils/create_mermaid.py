import json
from typing import List, Optional
from pathlib import Path
from ..models.roadmap import MermaidCourseData
from ..Logger import setup_logger


def generate_mermaid_timeline(course_data: MermaidCourseData, career_path) -> str:
    logging = setup_logger()
    logging.info("----------- Generate mermaid timeline ----------")
    """
    Generates a Mermaid timeline markdown string from the course data. 

    Attributes:
        course_data (MermaidCourseData): Course Data in mermaid format
        career_path (str): Career interest of user
    
    Returns:
        mermaid_code (str): Mermaid code in string
    
    Raises:
        Exception: Re-raises any unexpected errors encountered during processing.

    """
    try:
        current_dir = Path(__file__).resolve().parent
        utils_dir = current_dir.parent
        
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
        with open(f"{utils_dir}/data/Careers_with_key.json", 'r', encoding='utf-8') as infile:
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
        return {"status": "success", 
                "result": mermaid_code}
    except Exception as e:
        logging.exception("Unexpected Error while generating mermaid timeline")
        return {
            "status": "error",
            "message": "Error while generating mermaid timeline"
        }

        

