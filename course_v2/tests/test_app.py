from streamlit.testing.v1 import AppTest

def test_login_page():
    """Test if Login page is displayed correctly when starting the app"""
    at = AppTest.from_file("app.py")

    # Mock user session state
    at.session_state.user = None
    at.run()

    assert ":woman-raising-hand: Welcome to NTUCourses" in at.title[0].value
    assert at.header[0].value == "Log in"
