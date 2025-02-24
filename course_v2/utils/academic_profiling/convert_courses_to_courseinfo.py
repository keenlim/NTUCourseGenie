from ..models.course import CourseInfo, CourseData
from typing import List, Dict
from ..Logger import setup_logger

def convert_courses_to_courseinfo(courses: List[dict]) -> List[CourseData]:
    """
    Convert a list of course dictionaries (returned from Courses) into a list of CourseInfo objects

    For each course dictionary, it extracts the 'Code' as courseCode.
    If 'CourseType' is missing, it defaults to 'C'.

    For each course dictionary:
      - 'Code' is used as courseCode.
      - 'CourseType' is used as courseType.
      - 'Year' indicates which field in CourseData the course belongs to.

    Attributes:
        courses (List[dict]): List of course dictionaries.

    Returns:
        CourseData: An instance of CourseData with courses grouped by year and semester.    
    """
    logging = setup_logger()
    logging.info("----------- Converting course to CourseInfo ----------")
    # Prepare a dictionary to collect courses per semester.
    grouped_courses: Dict[str, List[CourseInfo]] = {}

    for course in courses:
        year = course.get("Year")
        if not year:
            # If no 'Year' key is provided, skip this course.
            continue

        # Create a CourseInfo instance (using only the required fields)
        course_info = CourseInfo(
            courseCode=course.get("Code"),
            courseType=course.get("CourseType", "C")  # default to 'C' if missing
        )
        if year in grouped_courses:
            grouped_courses[year].append(course_info)
        else:
            grouped_courses[year] = [course_info]

    # Create a dictionary that maps each field in CourseData to the corresponding list,
    # using None for missing semesters.
    course_data_dict = {field: grouped_courses.get(field, None) for field in CourseData.model_fields}
    
    logging.info("---- Succesfully convert courses to courseInfo----")
    # Return an instance of CourseData.
    return CourseData(**course_data_dict).model_dump(by_alias=True)