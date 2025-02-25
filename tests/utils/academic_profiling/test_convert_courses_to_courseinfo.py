import pytest
from course_v2.utils.academic_profiling.convert_courses_to_courseinfo import convert_courses_to_courseinfo  # Adjust this import as needed
from course_v2.utils.models.course import CourseData      # Adjust this import as needed

def test_convert_courses_to_courseinfo_with_valid_data():
    """
    Test converting a list of courses with valid data.
    Courses are grouped by their 'Year' key. If 'CourseType' is missing,
    it should default to "C".
    """
    # Given: sample course dictionaries
    courses = [
        {"Year": "Year1", "Code": "CSC101", "CourseType": "C"},
        {"Year": "Year1", "Code": "CSC102"},  # Missing CourseType; should default to "C"
        {"Year": "Year2", "Code": "CSC201", "CourseType": "C"},
        {"Year": "Year3", "Code": "CSC301", "CourseType": "C"},
        {"Code": "CSC999", "CourseType": "C"},  # Missing Year; should be skipped.
    ]
    
    # When: converting courses
    result = convert_courses_to_courseinfo(courses)
    
    # Then: build expected output based on CourseData.model_fields
    expected = {}
    for field in CourseData.model_fields:
        if field == "Year1":
            expected[field] = [
                {"courseCode": "CSC101", "courseType": "C"},
                {"courseCode": "CSC102", "courseType": "C"}
            ]
        elif field == "Year2":
            expected[field] = [{"courseCode": "CSC201", "courseType": "C"}]
        elif field == "Year3":
            expected[field] = [{"courseCode": "CSC301", "courseType": "C"}]
        else:
            expected[field] = None

    assert result == expected

def test_convert_courses_to_courseinfo_empty():
    """
    Test that an empty list of courses results in all CourseData fields being None.
    """
    # Given: an empty list
    courses = []
    
    # When: converting courses
    result = convert_courses_to_courseinfo(courses)
    
    # Then: expected output should have None for every field in CourseData
    expected = {field: None for field in CourseData.model_fields}
    assert result == expected

def test_convert_courses_to_courseinfo_missing_year():
    """
    Test that courses missing the 'Year' key (or with an empty value)
    are skipped in the conversion.
    """
    # Given: courses missing a valid 'Year' key
    courses = [
        {"Code": "CSC101", "CourseType": "L"},                # Missing Year
        {"Year": "", "Code": "CSC102", "CourseType": "T"},      # Empty Year value
    ]
    
    # When: converting courses
    result = convert_courses_to_courseinfo(courses)
    
    # Then: expected output should have None for every field in CourseData
    expected = {field: None for field in CourseData.model_fields}
    assert result == expected
