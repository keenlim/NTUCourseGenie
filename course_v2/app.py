import os
import streamlit as st
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from streamlit_msal import Msal
from login_ui import login_ui

load_dotenv(override=True)

# Streamlit layout
st.set_page_config(page_title="NTUCourse", page_icon=":material/bookmarks:", layout="wide")

# Initialise App Registration
CLIENT_ID = os.environ['APP_REG_CLIENT_ID']
AUTHORITY = os.environ['AUTHORITY']
CLIENT_SECRET = os.environ['APP_REG_CLIENT_SECRET']

# Utils Functions: User authentication pages
def login():
    st.title(":woman-raising-hand: Welcome to NTUCourses")
    # Add a header
    st.header("Log in")
    login_ui()

# Logout 
def logout():
    st.query_params.clear()
    del st.session_state.user
    del st.session_state.email
    del st.session_state.auth_code
    del st.session_state.role
    st.rerun()

# Initialise session states if not already initialised
if "user" not in st.session_state:
    st.session_state.user = None 
if "email" not in st.session_state:
    st.session_state.email = None
if "auth_code" not in st.session_state:
    st.session_state.auth_code = None
if "oid" not in st.session_state:
    st.session_state.oid = None
if "mongodb" not in st.session_state:
    st.session_state.mongodb = None
if "year_standing" not in st.session_state:
    st.session_state.year_standing = None

if "name" not in st.session_state:
    st.session_state.name = None

if "role" not in st.session_state:
    st.session_state.role = None
  
ROLES = ["Student", "NewStudent"]
  
# Define all the pages
role = st.session_state.role

# Define your account pages
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

getStarted_page = st.Page("getStarted.py", title="Get Started!", icon=":material/start:", default=(role=="NewStudent"))
chatbot_page = st.Page("chatbot.py", title="Chat with Me!", icon=":material/chat:", default=(role=="Student"))
user_page = st.Page("user.py", title="View Profile", icon=":material/account_circle:")

# Group your pages into convenient lists
account_pages = [logout_page]
chatbot_pages = [chatbot_page, user_page]
user_pages = [getStarted_page]

# Initialise a dictionary of page lists.
page_dict = {}

if st.session_state.role in ["Student"]:
    page_dict["Student"] = chatbot_pages

if st.session_state.role in ["NewStudent"]:
    page_dict["Getting Started"] = user_pages


if len(page_dict) > 0:
    pg = st.navigation({"Account": account_pages} | page_dict)
  
else:
    pg = st.navigation([st.Page(login)])

pg.run()