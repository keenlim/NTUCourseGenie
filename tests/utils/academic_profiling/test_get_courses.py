import json
import pandas as pd
import pytest
from pathlib import Path

# Import the function to test. Adjust the module name as needed.
from course_v2.utils.academic_profiling.get_courses import get_courses

@pytest.fixture
def setup_data(tmp_path):
    """
    Sets up a temporary directory structure with the required JSON files.
    
    The directory structure will be:
      tmp_path/
          dummy/           <-- dummy directory to simulate __file__ location
              test.py      <-- dummy file whose path will be used for __file__
          data/
              courses_by_code.json
              CSC_schedule.json
              
    The __file__ of the module under test will be patched to tmp_path/dummy/test.py so that:
      current_dir = Path(__file__).resolve().parent   -> tmp_path/dummy
      utils_dir = current_dir.parent                  -> tmp_path
    And files will be looked up in: tmp_path/data
    """
    # Create a dummy directory and file to simulate __file__
    dummy_dir = tmp_path / "dummy"
    dummy_dir.mkdir()
    dummy_file = dummy_dir / "test.py"
    dummy_file.write_text("# dummy file for __file__ patching")
    
    # Create the data directory
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create courses_by_code.json
    courses_by_code = {
        "SC1003": {"title": "Intro to Comp Thinking"},
        "SC2003": {"title": "Advanced Comp Thinking"}
    }
    courses_by_code_path = data_dir / "courses_by_code.json"
    courses_by_code_path.write_text(json.dumps(courses_by_code))
    
    # Create CSC_schedule.json
    # For a "Normal" degree in cohort "2021", we simulate a schedule with two semesters in Year1.
    schedule = {
        "2021_Normal": {
            "Year1_Semester1": ["SC1003"],
            "Year1_Semester2": ["SC2003"],
            "Year1_SpecialSemester": None
        }
    }
    schedule_path = data_dir / "CSC_schedule.json"
    schedule_path.write_text(json.dumps(schedule))
    
    # Return the dummy_file path to be used for patching __file__
    return dummy_file

def test_get_courses_valid(tmp_path, monkeypatch, setup_data):
    """
    Test that get_courses correctly reads the files and returns a DataFrame
    with the expected courses.
    """
    dummy_file = setup_data
    # Patch __file__ in the module where get_courses is defined.
    # This ensures that the function looks for files in tmp_path/data.
    import course_v2.utils.academic_profiling.get_courses
    monkeypatch.setattr(course_v2.utils.academic_profiling.get_courses, "__file__", str(dummy_file))
    
    # Call the function with valid parameters.
    df = get_courses("CSC", "2021", "Normal", 1)
    
    # 
