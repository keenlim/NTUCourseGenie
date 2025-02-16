import time
import json
from uuid import uuid4
import streamlit as st
from pydantic import TypeAdapter
from pathlib import Path
from streamlit_mermaid import st_mermaid
from utils.create_mermaid import generate_mermaid_timeline, CourseData
from functions.app import app_response
from utils.generate_updated_roadmap import generate_updated_roadmap
from streamlit_feedback import streamlit_feedback
from langfuse_utils.langfuse_app import LangfuseApp

# Initialisation
degree = None
cohort = None
degree_key = None
degree_type = None
career = []
year_standing = None
user = None

if 'last_updated' not in st.session_state:
   st.session_state.last_updated = None

# Get Information from DB
db = st.session_state.mongodb
collection = db["users"]

# Get user information 
user = collection.find_one({"_id": st.session_state.oid})
st.session_state.last_updated = user['last_updated']
st.session_state.courseDetail = user['coursedata']
st.session_state.career_output = user['career_path']

degree = st.session_state.last_updated.get('degree', None)
cohort = st.session_state.last_updated.get('cohort', None)
degree_key = st.session_state.last_updated.get('degree_key', None)
degree_type = st.session_state.last_updated.get('degree_type', None)
career = st.session_state.last_updated.get('career', None)
year_standing = st.session_state.last_updated.get('year_standing', None)

years = ["Year1_Semester1", "Year1_Semester2", "Year2_Semester1", "Year2_Semester2", "Year3_Semester1", "Year3_Semester2", "Year4_Semester1", "Year4_Semester2", "Year5_Semester1", "Year5_Semester2", "Year1_SpecialSemester", "Year3_SpecialSemester"]

file_name = f"{degree_key}_schedule.json"

current_dir = Path(__file__).parent
with open(f"{current_dir}/utils/data/{file_name}", "r") as f:
   data = json.load(f)

with open(f"{current_dir}/ui/initial_message.md", "r") as message_file:
    MESSAGE_CONTENT = message_file.read()

def get_course_data():
   # Utils: Generate Mermaid Diagram
   course_dict = {}
   for program_name, program_data in data.items():
      course_data = TypeAdapter(CourseData).validate_python(program_data)
      course_dict[program_name] = course_data
   
   return course_dict

# TODO: Should Generate Roadmap in getStarted page and saved it in DB
with st.spinner(text="Preparing Chatbot"):
   if user.get('generated_course', None) is not None:
      converted_generated_course = user.get('generated_course', None)
      # print(converted_generated_course)
      mermaid_code = generate_mermaid_timeline(TypeAdapter(CourseData).validate_python(converted_generated_course), career[0])
      # print(mermaid_code)
   else:
      if st.session_state.courseDetail is not None:
         # generated_course should just retrieve from DB
         # Generate based on courses users already taken (Applicable if users are not Prospective Students)
         
         # TODO: Simple try and except to catch the error in case LLM does not structure it well
         try:
            generated_course = generate_updated_roadmap(get_course_data()[f"{cohort}_{degree_type}"], st.session_state.courseDetail)
            user_data = {
               "generated_course": generated_course.dict()
            }
         except:
            user_data = {"generated_course": None}
         # Get user
         if user is not None:
            result = collection.update_one(
               {"_id": st.session_state.oid}, {"$set": user_data}, upsert=True
            )
            print("Updated generated course into DB")
         mermaid_code = generate_mermaid_timeline(generated_course, career[0])
         # print(mermaid_code)
      # Get the pre-defined roadmap based on Career and course details
      else:
         mermaid_code = generate_mermaid_timeline(get_course_data()[f"{cohort}_{degree_type}"], career[0])

# Utils: Submit Feedback Utils
def _submit_feedback(user_response, run_id):
    print("Feedback submitted")
    st.toast(f"Feedback submitted")
    print(user_response)
   #  print(emoji)
    print(run_id)

    score_to_dict = {
       '😞': 0.2,
       '🙁': 0.4,
       '😐': 0.6,
       '🙂': 0.8,
       '😀': 1.0,
       '👎': 0.0, 
       '👍': 1.0,
    }

    # Add score to Langfuse
    log_langfuse = LangfuseApp().add_langfuse_score(run_id, score_to_dict[user_response['score']], user_response['text'])

    return user_response.update({"Langfuse Status": log_langfuse})

feedback_kwargs = {
        "feedback_type": "faces",
        "optional_text_label": "Please provide extra information",
        "on_submit": _submit_feedback,
    }

# Utils: Display Chat Messages
def display_chat_messages() -> None:
   """
   Print message history
   @returns None
   """
   for n, message in enumerate(st.session_state.messages):
      with st.chat_message(message["role"]):
         st.markdown(message["content"], unsafe_allow_html=True)
      
      if message["role"] == "assistant" and n > 0:
         feedback_key = f"feedback_{message["run_id"]}"

         if feedback_key not in st.session_state:
            st.session_state[feedback_key] = None
         
         disable_with_score = (
                st.session_state[feedback_key].get("score")
                if st.session_state[feedback_key]
                else None
            )
         streamlit_feedback(
               **feedback_kwargs,
               key=feedback_key,
               disable_with_score=disable_with_score,
               kwargs={"run_id": message["run_id"]}
         )

# Utils: Streamed response emulator
def response_generator(response):
   for word in response.split():
      yield word + " "
      time.sleep(0.05)

def stream_response(response):
   placeholder = st.empty()
   text = ''
   for char in response:
      text += char
      placeholder.markdown(text)
      time.sleep(0.02) # Adjust the speed as needed 
   
   # Return an empty string to prevent 'None' from being displayed
   return ''

# Add Course
@st.dialog("Add Course Code")
def add_course():
   print("ADD COURSE")
   year = st.selectbox(label="Year", options=years)
   courseCode = st.text_input("Course Code")
   if st.button("ADD Course", use_container_width=True):
      print(courseCode, year)
      # Add it into generated_code and update DB
      generated_code = user.get('generated_course', None)
      generated_code[year].append(courseCode)
      print(generated_code)
      # Update DB
      user_data = {
         "generated_course": generated_code
      }
      # Get user
      if user is not None:
         result = collection.update_one(
            {"_id": st.session_state.oid}, {"$set": user_data}, upsert=True
         )
         print("Updated generated course into DB", result)
      st.rerun()

@st.dialog("Delete Course Code")
def delete_course():
   print("DELETE COURSE")
   year = st.selectbox(label="Year", options=years)
   courseCode = st.text_input("Course Code")
   if st.button("DELETE Course", use_container_width=True):
      generated_code = user.get('generated_course', None)
      if courseCode in generated_code[year]:
         generated_code[year].remove(courseCode)
         # Update DB
         user_data = {
            "generated_course": generated_code
         }
         # Get user
         if user is not None:
            result = collection.update_one(
               {"_id": st.session_state.oid}, {"$set": user_data}, upsert=True
            )
            print("Updated generated course into DB", result)
      else:
         st.warning("Course Code is not found", icon="⚠️")
      st.rerun()
      

@st.dialog("Replace Course Code")
def replace_course():
   print("REPLACE COURSE")
   year = st.selectbox(label="Year", options=years)
   old_courseCode = st.text_input("Course Code to be replaced")
   new_courseCode = st.text_input("New Course Code")
   if st.button("REPLACE Course",use_container_width=True):
      generated_code = user.get('generated_course', None)
      if old_courseCode in generated_code[year]:
         idx = generated_code[year].index(old_courseCode)
         generated_code[year][idx] = new_courseCode

         user_data = {
            "generated_course": generated_code
         }
         # Get user
         if user is not None:
            result = collection.update_one(
               {"_id": st.session_state.oid}, {"$set": user_data}, upsert=True
            )
            print("Updated generated course into DB", result)
      else:
         st.warning("Course Code is not found", icon="⚠️")
      
      st.rerun()

# Streamlit FE Code 
# App Title
gradient_text_html = """
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
<div class="gradient-text">CourseGenie.</div>
"""

st.markdown(gradient_text_html, unsafe_allow_html=True)
st.caption("Ask anything about your Course and Degree!")

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

# Initialise the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = []
    st.session_state.greetings = False
   
if "chat_id" not in st.session_state.keys():
   st.session_state.chat_id = str(uuid4())

# Greet User
with st.chat_message("assistant"):
   st.markdown(MESSAGE_CONTENT)
   st.subheader(f"NTU Roadmap - {degree_key} | {cohort} | {degree_type} | {st.session_state.career_output.get('career', None) if st.session_state.career_output else st.session_state.last_updated.get('career', None)[0]}")
   st_mermaid(mermaid_code, width="auto", show_controls=False, zoom=False, pan=False)

   # Edit mermaid diagram via code
   col1, col2, col3 = st.columns(3)
   with col1:
      if st.button("Add Course", use_container_width=True, icon=":material/add:"):
         add_course()
   with col2:
      if st.button("Replace Course", use_container_width=True, icon=":material/adjust:"):
         replace_course()
   with col3:
      if st.button("Delete Course", use_container_width=True, icon=":material/close:"):
         delete_course()

   if st.session_state.career_output:
      with st.expander("See explanation"):
         st.write(st.session_state.career_output.get("explanation", None))
      st.success(st.session_state.career_output.get('strength', None), icon="✅")
      st.warning(st.session_state.career_output.get('weakness', None), icon="⚠️")


display_chat_messages()

# ------------- Main Chat Logic Starts Here --------------------
if prompt:= st.chat_input("Ask Anything"):
   # Display user message in chat message
   with st.chat_message("user"):
      st.markdown(prompt)
   
   # Add user message to chat history
   st.session_state.messages.append({"role": "user", "content": prompt})

   # ----- Add AI Assistant Response Logic -------
   # Display + Add Assistant response to chat history
   with st.chat_message("assistant"):
      # print(st.session_state.messages)
      response, run_id= app_response(prompt, st.session_state.chat_id, st.session_state.messages, st.session_state.last_updated, st.session_state.oid)
      st.markdown(stream_response(response))
      st.session_state.messages.append({"role": "assistant", "content": response, "run_id": run_id, "feedback":False})

      streamlit_feedback(
            **feedback_kwargs, key=f"feedback_{run_id}", kwargs={"run_id": run_id}
        )


   