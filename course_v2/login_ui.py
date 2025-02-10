import os
import time
import requests
import streamlit as st 
from io import BytesIO
from dotenv import load_dotenv
from msal import ConfidentialClientApplication
from texts import LongText
from utils.Logger import setup_logger
from utils.Database.DBConnector import DBConnector

load_dotenv(override=True)

CONNECTION_STRING = os.environ.get("MONGODB_HOST")
DB_NAME = os.environ.get("DATABASE_NAME")

def initialize_app():
    client_id = os.getenv("APP_REG_CLIENT_ID")
    client_secret = os.getenv("APP_REG_CLIENT_SECRET")
    authority_url = os.getenv("AUTHORITY")

    app = ConfidentialClientApplication(
        client_id=client_id,
        authority=authority_url,
        client_credential=client_secret
    )

    return app

def get_auth_url(app):
    auth_url = app.get_authorization_request_url(
        scopes = ["User.Read"],
    )
    return auth_url

def get_token_from_code(app, auth_code):
    result = app.acquire_token_by_authorization_code(
        auth_code, 
        scopes=["User.Read"],
    )
    return result

def get_user_photo(user_object_id, access_token):
    # Make a GET request to the Microsoft Graph APi
    headers = {"Authorization": "Bearer " + access_token}
    response = requests.get(f"https://graph.microsoft.com/v1.0/users/{user_object_id}/photo/$value", headers=headers)
    if response.status_code == 200:
        # Convert the binary data to a BytesIO object
        image_data = BytesIO(response.content)
        return image_data
    else:
        return None

def unauthorise(progress_bar, progress_text, error_msg):
    st.query_params.clear()
    del st.session_state.user
    del st.session_state.email
    del st.session_state.auth_code
    progress_bar.progress(100, text=progress_text)

    st.error(error_msg)
    st.button("Retry")

    time.sleep(2)
    progress_bar.empty()

def login_ui():
    informed_consent_form = st.empty()
    # Initialise Logger
    logger = setup_logger()
    logger.info("----------- New state ----------")

    # Initialise App Registration
    app = initialize_app()

    # Check if user has not signed in
    if st.session_state.user is None:
        st.session_state.auth_code = st.query_params.get("code")
        # Clear query parameters
        st.query_params.clear()
        if st.session_state.auth_code is None:
            logger.info("No auth code found, displaying consent form")
            with informed_consent_form.container():
                # Display consent form
                with st.container(height=300):
                    st.markdown(LongText.TERMS_OF_USE)
                st.checkbox(LongText.CONSENT_ACKNOWLEDGEMENT, key="agree_check")
                cols = st.columns(4)

                # Display buttons
                with cols[0]:
                    btn_agree = st.button("Agree and Proceed", disabled=not st.session_state.agree_check)
            
            # If user has agrees to the terms of use
            if btn_agree:
                informed_consent_form.empty()
                auth_url = get_auth_url(app)
                st.markdown(
                    f"To prevent unauthorised usage and abuse of the system, we will need you to verify that you are an NTU "
                    f"student. Please follow the verification process below to continue..."
                )
                st.markdown(f'<a href="{auth_url}" target="_self">Proceed to Verification</a>', unsafe_allow_html=True)
                progress_bar = st.progress(0, text="Please click the link above to verify.")
        
        # When user was redirected back from the authenticated page with an auth code in url params
        else:
            logger.info("Auth code found, attempting to get token")
            progress_bar = st.progress(20, text="Authenticating...")
            result = get_token_from_code(app, st.session_state.auth_code)
            logger.info(f"access_token found in result")
            # If login is successful
            if "access_token" in result:
                logger.info("Token is valid and saved to local storage")
                progress_bar.progress(50, text="Retrieving and checking profile...")

                # Get user profile
                st.session_state.user_photo = get_user_photo(result['id_token_claims']['oid'], result['access_token'])
                st.session_state.user = result['id_token_claims']['name']
                st.session_state.email = result['id_token_claims']['preferred_username']
                st.session_state.formatted_name = st.session_state.user.replace("#", "")
                st.session_state.oid = result['id_token_claims']['oid'] # dfd4ed12-16a9-443f-b19f-dc2b8cd90b9e

                logger.info(st.session_state.user)

                # Check for ntu email
                if "ntu.edu.sg" in st.session_state.email[-10:]:
                    progress_bar.progress(70, text="Waking up NTU Course")

                    # Check if it is an existing student in the DB 
                    # IF it does --> Means is student --> Straight to the chatbot
                    # Access the Database
                    db = DBConnector(CONNECTION_STRING).get_db(DB_NAME)
                    st.session_state.mongodb = db
                    collection = db["users"]
                    doc = collection.find_one({"_id": st.session_state.oid})
                    # print(doc)
                    if doc is not None:
                        st.session_state.role = "Student"
                        progress_bar.progress(100, text="NTU Course is Ready!")
                        time.sleep(1)
                        progress_bar.empty()
                        st.rerun()

                    # ELSE --> NewStudent --> New student need to go through the get started page 
                    else:
                        st.session_state.role = "NewStudent"
                        progress_bar.progress(100, text="NTU Course is Ready!")
                        time.sleep(1)
                        progress_bar.empty()
                        st.rerun()
                
                else:
                    unauthorise(progress_bar, 
                                progress_text = "Unauthrorised user...",
                                error_msg = "Please veryfiy using your NTU email address.")
            
            # Login failed
            else:
                logger.error("Authentication failed")
                st.write(result.get("error"))
                st.write(result.get("error_description"))
                st.write(result.get("correlation_id")) # You may need this when reporting a bug
