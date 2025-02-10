import json
import streamlit as st
from utils.get_courses import get_courses
from utils.analyse_image import analyse_image, analyse_course_image
from utils.feedback_career import career_feedback
import base64
from utils.generate_updated_roadmap import generate_updated_roadmap
from pydantic import TypeAdapter
from utils.create_mermaid import CourseData
from pathlib import Path
current_dir = Path(__file__).parent

# st.write(st.session_state)


# Buttons Utils
def auto_fill_btn():
    st.session_state.autoFill = True
    st.session_state.last_updated = {
        "degree": degree,
        "cohort": cohort,
        "degree_key": degree_key, 
        "degree_type": degree_type, 
        "career": career, 
        "year_standing": year_standing,
        "semester": semester
        }
    # print(st.session_state.last_updated)
    all_course = []
    image_uploaded = []
    print("Analysing Image")
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.getvalue()
        encoded = base64.b64encode(bytes_data).decode("utf-8")
        image_uploaded.append(encoded)
        response = analyse_image(encoded).dict(by_alias=True)
        all_course.extend(response['Course'])
    
    st.session_state.imageData = image_uploaded
    st.session_state.courseData = all_course
    # print(st.session_state.courseData)

def get_course_data(degree_key):
   # Utils: Generate Mermaid Diagram
   file_name = f"{degree_key}_schedule.json"
   with open(f"{current_dir}/utils/data/{file_name}", "r") as f:
       data = json.load(f)
   course_dict = {}
   for program_name, program_data in data.items():
      course_data = TypeAdapter(CourseData).validate_python(program_data)
      course_dict[program_name] = course_data
   
   return course_dict
# Options Utils
DEGREE_OPTIONS = {"CE": "Computer Engineering", "CSC": "Computer Science", "DSAI": "Data Science and Artificial Intelligence", "BCE": "Double Degree in Computer Engineering and Business", "CEEcons": "Double Degree in Computer Engineering and Economics", "BCG": "Double Degree in Computer Science and Business", "CSEcons": "Double Degree in Computer Science and Economics"}
COHORT = ["2021", "2022", "2023", "2024"]
DEGREE_TYPE = {"CE": ["Normal", "Poly", "ABP"],
               "CSC": ["Normal", "Poly", "ABP"],
               "DSAI": ["Normal"],
               "BCE": ["Normal"],
               "CEEcons": ["PI", "PA"],
               "BCG": ["Normal"],
               "CSEcons": ["PI", "PA"]}
CAREER_OPTIONS = ["Blockchain Engineer", "DevOps Engineer", "Cloud Engineer/Architect", "Mixed/Virtual Reality Developer", "Cyber Security", "Software Engineer", "Full-stack Developer", "Front-End Engineer / Web Developer", "Backend Engineer", "Data Engineer", "Business Analyst", "Firmware Engineer", "Computer Hardware Engineer", "Embedded System Developer","AI Engineer", "Machine Learning Engineer", "Data Scientist", "Data Analyst", "AI Scientist", "System Architect", "Cybersecurity Consultant/Analyst", "Product Manager", "Entrepreneur", "Quantitative Analyst/Developer"]
YEAR_STANDING = {0:"Prospective Student", 1:"Year 1", 2:"Year 2", 3:"Year 3", 4:"Year 4", 5:"Year 5"}
SEMESTER = ["Semester 1", "Semester 2", "Not applicable"]

generated_course = None
# Initialise values in Session State
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = {"degree": list(DEGREE_OPTIONS.values())[0], "cohort": COHORT[0],"degree_key": list(DEGREE_OPTIONS.keys())[0], "degree_type": DEGREE_TYPE[list(DEGREE_OPTIONS.keys())[0]][0], "career": None, "year_standing": list(YEAR_STANDING.values())[0],"semester": SEMESTER[0]}
if 'courseData' not in st.session_state:
    st.session_state.courseData = None
if 'career' not in st.session_state:
    st.session_state.career = None
if 'career_output' not in st.session_state:
    st.session_state.career_output = None
if 'imageData' not in st.session_state:
    st.session_state.imageData = None
if 'courseDetail' not in st.session_state:
    st.session_state.courseDetail = None

# Sidebar
with open(f"{current_dir}/ui/sidebar.md", "r") as sidebar_file:
    sidebar_content = sidebar_file.read()

with open(f"{current_dir}/ui/feedback.md", "r") as feedback_file:
   feedback_content = feedback_file.read()

with st.sidebar:
   st.markdown(feedback_content)
   st.link_button("Feedback", url="https://forms.office.com/r/u7KXJPsmfp", help="Provide feedback to help me improve!", type="secondary", icon="🔔", use_container_width=True)
   st.markdown(sidebar_content)

with open(f"{current_dir}/ui/styles.md", "r") as styles_file:
    styles_content = styles_file.read()

st.write(styles_content, unsafe_allow_html=True)


gradient_title_html = """
<style>
.gradient-text {
    font-weight: bold;
    background: -webkit-linear-gradient(left, red, orange);
    background: linear-gradient(to right, red, orange);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline;
    font-size: 3em;
}
</style>
<div class="gradient-text">Edit Profile.</div>
"""

st.markdown(gradient_title_html, unsafe_allow_html=True)

st.write(f"Update your profile information")

# st.write(st.session_state)

st.subheader("Academic Standing")
degree = st.selectbox("Degree", options=DEGREE_OPTIONS.values(), index=list(DEGREE_OPTIONS.values()).index(st.session_state.last_updated['degree']))

col1, col2, col3, col4 = st.columns(4)
with col1:
    cohort = st.selectbox("Cohort", options = COHORT, index=COHORT.index(st.session_state.last_updated['cohort']))
with col2:
    degree_key = list(filter(lambda x: DEGREE_OPTIONS[x] == degree, DEGREE_OPTIONS))[0]
    degree_type = st.selectbox("Degree Type", options = DEGREE_TYPE[degree_key], index=DEGREE_TYPE[degree_key].index(st.session_state.last_updated['degree_type']) if st.session_state.last_updated['degree_type'] in DEGREE_TYPE[degree_key] else 0)
with col3:
    year_standing = st.selectbox("Year Standing", options=YEAR_STANDING.values(), index=list(YEAR_STANDING.values()).index(st.session_state.last_updated['year_standing']))
with col4:
    semester = st.selectbox("Most Recently Completed Semester", options=SEMESTER, index=SEMESTER.index(st.session_state.last_updated['semester']))

st.subheader("Career Intersts and Goals")
career = st.multiselect("Career Interest", options=CAREER_OPTIONS, default=st.session_state.last_updated['career'])

if year_standing in ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]:
    st.subheader("For Current Students: ")
    st.write("You can choose to upload a screenshot of your degree audit that provides the courses information and grades OR choose to manually provide the course information in the table below.")
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()

    if uploaded_files:
        st.button("Auto Fill Courses", use_container_width=True, on_click=auto_fill_btn, icon=":material/edit:")
    
    # Get the year_standing key to be passed in the later function
    year = list(filter(lambda x: YEAR_STANDING[x]==year_standing, YEAR_STANDING))[0]

    if st.session_state.courseData:
        DATA = st.session_state.courseData
    else: 
        DATA = get_courses(degree_key, cohort, degree_type, year)
    
    # Table format that provides all Mods
    edited_df = st.data_editor(DATA, num_rows="dynamic", use_container_width=True)
    # print(edited_df)

# Every form must have a submit button.
submitted = st.button("Update", use_container_width=True, icon=":material/send:")
if submitted:
    # TODO: Save these entries into DB
    st.session_state.role = "Student"
    st.session_state.last_updated = {
        "degree": degree,
        "cohort": cohort,
        "degree_key": degree_key, 
        "degree_type": degree_type, 
        "career": career, 
        "year_standing": year_standing,
        "semester": semester
        }
    course_details = []
    if year_standing in ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]:
        # Set Career Interest to the st.session_state
        career_feedback_output = career_feedback(st.session_state.last_updated.get('degree', None), st.session_state.last_updated.get('career', None), edited_df)
        # print(career_feedback_output)

        st.session_state.career_output = career_feedback_output.dict()
        # print(st.session_state.career_output)
        if st.session_state.imageData:
            for image in st.session_state.imageData:
                course_response = analyse_course_image(image).dict(by_alias=True)
                # print(course_response)
                course_details.append(course_response)
            st.session_state.courseDetail = course_details
        # print(st.session_state.courseDetail)

    # Just take the first career interest that the user select
    # For the recommended roadmap
    # With User SSO Login, these results should be saved to the DB --> Only when users click on submit then saved it in DB
    if course_details is not None:
        # Generate based on courses users already taken (Applicable if users are not Prospective Students)
        generated_course = generate_updated_roadmap(get_course_data(degree_key)[f"{cohort}_{degree_type}"], st.session_state.courseDetail)
        user_data = {
            "generated_course": generated_course.dict()
        }
    user = {
        "userId": st.session_state.oid,
        "name": st.session_state.user,
        "email": st.session_state.email,
        "last_updated": st.session_state.last_updated,
        "coursedata": st.session_state.courseDetail,
        "career_path": st.session_state.career_output,
        "generated_course": generated_course.dict() if generated_course is not None else None
    }

    db = st.session_state.mongodb
    collection = db["users"]
    # Check if the user is already in the DB
    doc = collection.find_one({"_id": user["userId"]})
    if doc is None:
        result = collection.update_one(
            {"_id": user["userId"]}, {"$set": user}, upsert=True
        )
        print("Upserted document with _id {}\n".format(result.upserted_id))
        st.success("Updated User Profile", icon="✅")
    
    else:
        result = collection.update_one(
            {"_id": user["userId"]}, {"$set": user}, upsert=True
        )
        print("Upserted document with _id {}\n".format(user["userId"]))
        st.success("Updated User Profile", icon="✅")

    st.rerun()



