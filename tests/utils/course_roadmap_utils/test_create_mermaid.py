import json
import pytest
from pathlib import Path

# Assume that generate_mermaid_timeline is imported from your module.
from course_v2.utils.course_roadmap_utils.create_mermaid import generate_mermaid_timeline

# Create a dummy MermaidCourseData for testing purposes.
class DummyMermaidCourseData:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

@pytest.fixture
def setup_mermaid_files(tmp_path):
    """
    Sets up a temporary directory structure with:
    - A dummy file to simulate __file__ (e.g., tmp_path/dummy/test.py).
    - A data directory (tmp_path/data) containing a Careers_with_key.json file.
    Returns the dummy file path and the data directory.
    """
    # Create a dummy directory and file to simulate the module file location.
    dummy_dir = tmp_path / "dummy"
    dummy_dir.mkdir()
    dummy_file = dummy_dir / "test.py"
    dummy_file.write_text("# dummy file for __file__ patching")
    
    # Create the data directory.
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create Careers_with_key.json with valid career data.
    career_data = {
        "Data Science": {
            "electives": ["Elective1", "Elective2"]
        }
    }
    careers_file = data_dir / "Careers_with_key.json"
    careers_file.write_text(json.dumps(career_data))
    
    return dummy_file, data_dir

def test_generate_mermaid_timeline_with_career(setup_mermaid_files, monkeypatch):
    """
    Test that the timeline is generated correctly when the career_path exists.
    The expected output should include the timeline sections for the provided years
    and append a recommended section for the given career.
    """
    dummy_file, _ = setup_mermaid_files
    # Patch __file__ in the module so that the function uses our temporary directory.
    import course_v2.utils.course_roadmap_utils.create_mermaid
    monkeypatch.setattr(course_v2.utils.course_roadmap_utils.create_mermaid, "__file__", str(dummy_file))
    
    # Create dummy course data with courses in Year1 and Year2.
    course_data = DummyMermaidCourseData(
        Year1_Semester1=["CourseA", "CourseB"],
        # Year1_Semester2 and Year1_SpecialSemester are omitted (None)
        Year2_Semester1=["CourseC"],
        Year2_Semester2=["CourseD"],
        Year2_SpecialSemester=["CourseE"]
    )
    
    result = generate_mermaid_timeline(course_data, "Data Science")
    assert result["status"] == "success"
    mermaid_result = result["result"]
    
    # Verify that the timeline header and sections are present.
    assert "timeline" in mermaid_result
    assert "Section Year_1" in mermaid_result
    assert "Year1_Semester1: CourseA : CourseB" in mermaid_result
    assert "Section Year_2" in mermaid_result
    assert "Year2_Semester1: CourseC" in mermaid_result
    assert "Year2_Semester2: CourseD" in mermaid_result
    assert "Year2_SpecialSemester: CourseE" in mermaid_result
    
    # Verify that the recommended section is appended.
    assert "Section Recommended_MPE:" in mermaid_result
    assert "MPE: Elective1 : Elective2" in mermaid_result

def test_generate_mermaid_timeline_without_career(setup_mermaid_files, monkeypatch):
    """
    Test that the timeline is generated correctly when the provided career_path does not exist.
    In this case, the recommended section should not be appended.
    """
    dummy_file, _ = setup_mermaid_files
    import course_v2.utils.course_roadmap_utils.create_mermaid
    monkeypatch.setattr(course_v2.utils.course_roadmap_utils.create_mermaid, "__file__", str(dummy_file))
    
    # Create dummy course data with only Year1 information.
    course_data = DummyMermaidCourseData(
        Year1_Semester1=["CourseA", "CourseB"]
    )
    
    result = generate_mermaid_timeline(course_data, "NonExistentCareer")
    assert result["status"] == "success"
    mermaid_result = result["result"]
    
    # Check for timeline and course sections.
    assert "timeline" in mermaid_result
    assert "Section Year_1" in mermaid_result
    assert "Year1_Semester1: CourseA : CourseB" in mermaid_result
    # The recommended section should not be present.
    assert "Section Recommended_MPE:" not in mermaid_result

def test_generate_mermaid_timeline_file_error(tmp_path, monkeypatch):
    """
    Test that the function returns an error status if Careers_with_key.json is missing.
    In this case, attempting to open the file should raise an exception, which is caught,
    and an error dictionary is returned.
    """
    # Setup a dummy __file__ in a temporary directory.
    dummy_dir = tmp_path / "dummy"
    dummy_dir.mkdir()
    dummy_file = dummy_dir / "test.py"
    dummy_file.write_text("# dummy file for __file__ patching")
    
    # Create a data directory WITHOUT the Careers_with_key.json file.
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    import course_v2.utils.course_roadmap_utils.create_mermaid
    monkeypatch.setattr(course_v2.utils.course_roadmap_utils.create_mermaid, "__file__", str(dummy_file))
    
    # Create dummy course data.
    course_data = DummyMermaidCourseData(
        Year1_Semester1=["CourseA"]
    )
    
    result = generate_mermaid_timeline(course_data, "Data Science")
    assert result["status"] == "error"
    assert "Error while generating mermaid timeline" in result["message"]
