import json
import streamlit as st
from utils.academic_profiling.get_courses import get_courses
from utils.academic_profiling.feedback_career import career_feedback
from utils.course_roadmap_utils.generate_updated_roadmap import generate_updated_roadmap
from pydantic import TypeAdapter
from utils.models.roadmap import MermaidCourseData
from pathlib import Path
from utils.academic_profiling.process_files import process_files
from utils.user_configuration.options_utils import Options
from utils.academic_profiling.convert_courses_to_courseinfo import convert_courses_to_courseinfo
from utils.models.user import LastUpdatedModel
from utils.Logger import setup_logger
current_dir = Path(__file__).parent

# st.write(st.session_state)

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
    
    upload_results = process_files(uploaded_files)
    
    if upload_results['status'] == "error":
        st.toast(upload_results['message'], icon="🚨")
    elif upload_results['status'] == "success": 
        st.toast("Succesfully uploaded degree audit", icon="🎉")
    
    st.session_state.imageData = upload_results["imageData"]
    st.session_state.courseData = upload_results["courseData"]

def get_course_data(degree_key):
   # Utils: Generate Mermaid Diagram
   file_name = f"{degree_key}_schedule.json"
   with open(f"{current_dir}/utils/data/{file_name}", "r") as f:
       data = json.load(f)
   course_dict = {}
   for program_name, program_data in data.items():
      course_data = TypeAdapter(MermaidCourseData).validate_python(program_data)
      course_dict[program_name] = course_data
   
   return course_dict

# Logging utils
logging = setup_logger()

# Options Utils
options = Options()
DEGREE_OPTIONS = options.degree_options()
COHORT = options.cohort_options()
DEGREE_TYPE = options.degree_type_options()
CAREER_OPTIONS = options.career_options()
YEAR_STANDING = options.year_standing_options()
SEMESTER = options.semester_options()

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
degree = st.selectbox("Degree *", options=DEGREE_OPTIONS.values(), index=list(DEGREE_OPTIONS.values()).index(st.session_state.last_updated['degree']))

col1, col2, col3, col4 = st.columns(4)
with col1:
    cohort = st.selectbox("Cohort *", options = COHORT, index=COHORT.index(st.session_state.last_updated['cohort']))
with col2:
    degree_key = list(filter(lambda x: DEGREE_OPTIONS[x] == degree, DEGREE_OPTIONS))[0]
    degree_type = st.selectbox("Degree Type *", options = DEGREE_TYPE[degree_key], index=DEGREE_TYPE[degree_key].index(st.session_state.last_updated['degree_type']) if st.session_state.last_updated['degree_type'] in DEGREE_TYPE[degree_key] else 0)
with col3:
    year_standing = st.selectbox("Year Standing *", options=YEAR_STANDING.values(), index=list(YEAR_STANDING.values()).index(st.session_state.last_updated['year_standing']))
with col4:
    semester = st.selectbox("Most Recently Completed Semester *", options=SEMESTER, index=SEMESTER.index(st.session_state.last_updated['semester']))

st.subheader("Career Interests and Goals *")
career = st.multiselect("Career Interest", options=CAREER_OPTIONS, default=st.session_state.last_updated['career'])

if year_standing in ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]:
    st.subheader("For Current Students: ")
    st.write("You may upload your degree audit in PDF or image format containing your course information and grades. Alternatively, you can manually enter the course details in the table below.")
    uploaded_files = st.file_uploader("Choose a file", accept_multiple_files=True, type=['png', 'jpg', 'jpeg', 'pdf'])

    if uploaded_files:
        st.button("Auto Fill Courses", use_container_width=True, on_click=auto_fill_btn, icon=":material/edit:")
    
    # Get the year_standing key to be passed in the later function
    year = list(filter(lambda x: YEAR_STANDING[x]==year_standing, YEAR_STANDING))[0]

    if st.session_state.courseData:
        DATA = st.session_state.courseData
    else: 
        try:
            DATA = get_courses(degree_key, cohort, degree_type, year)
            st.session_state.courseData = DATA
        except:
            DATA = None 
            st.error("Unable to retrieve course information, please report the error")
    
    # Table format that provides all Mods
    edited_df = st.data_editor(DATA, num_rows="dynamic", use_container_width=True)
    # print(edited_df)

# Every form must have a submit button.
try: 
    data = {
            "degree": degree,
            "cohort": cohort,
            "degree_key": degree_key, 
            "degree_type": degree_type, 
            "career": career, 
            "year_standing": year_standing,
            "semester": semester
        }

        # Validate the data model using Pydantic Model
    validated_data = LastUpdatedModel(**data)
    submitted = st.button("Update", use_container_width=True, icon=":material/send:")
except Exception as e:
    submitted = st.button("Update", use_container_width=True, icon=":material/send:", disabled=True, help=f"🚨 Please fill in all the required fields to continue.")
if submitted:
    st.session_state.role = "Student"
    data = {
        "degree": degree,
        "cohort": cohort,
        "degree_key": degree_key, 
        "degree_type": degree_type, 
        "career": career, 
        "year_standing": year_standing,
        "semester": semester
    }
    st.session_state.last_updated = data
    course_details = []
    if year_standing in ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]:
        # Set Career Interest to the st.session_state
        career_feedback_output = career_feedback(st.session_state.last_updated.get('degree', None), st.session_state.last_updated.get('career', None), edited_df)

        st.session_state.career_output = career_feedback_output.dict()
        st.session_state.courseDetail = convert_courses_to_courseinfo(st.session_state.courseData)
        generated_response = generate_updated_roadmap(get_course_data(degree_key)[f"{cohort}_{degree_type}"], st.session_state.courseDetail)
        if generated_response.get("status", None) == "success": 
            generated_course = generated_response.get("result", None).dict()
            logging.info("Succesfully generate updated course roadmap")
        else:
            generated_course = None
            logging.error(f"Error generating updated course roadmap, {generated_response.get("message", None)}")
        user_data = {
            "generated_course": generated_course
        }
    
    else:
        st.session_state.courseDetail = []
        generated_course = None
        user_data = {
            "generated_course": None
        }        
    

    user = {
        "userId": st.session_state.oid,
        "name": st.session_state.user,
        "email": st.session_state.email,
        "last_updated": st.session_state.last_updated,
        "coursedata": st.session_state.courseDetail,
        "career_path": st.session_state.career_output,
        "generated_course": generated_course if generated_course is not None else None
    }

    db = st.session_state.mongodb
    collection = db["users"]
    # Check if the user is already in the DB
    doc = collection.find_one({"_id": user["userId"]})
    if doc is None:
        result = collection.update_one(
            {"_id": user["userId"]}, {"$set": user}, upsert=True
        )
        logging.info("Upserted document with _id {}\n".format(result.upserted_id))
        st.toast("Succesfully updated user profile", icon="🎉")
    
    else:
        result = collection.update_one(
            {"_id": user["userId"]}, {"$set": user}, upsert=True
        )
        logging.info("Upserted document with _id {}\n".format(user["userId"]))
        st.toast("Succesfully updated user profile", icon="🎉")



