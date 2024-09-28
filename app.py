import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

from sections.agent_py_programmer import *
from sections.chatbot import *
from sections.software_engineer_basics import *

# Set page configuration to collapse the sidebar by default
st.set_page_config(
    page_title="Streamlit SAAS Tempalte",
    page_icon=":guardsman:",  # Optional, just adds an icon
    layout="centered",
    initial_sidebar_state="collapsed",  # This makes the sidebar collapsed by default
)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Login
authenticator.login()

# Authenticating users
if st.session_state["authentication_status"]:
    authenticator.logout()

    # Define available functions/subpages
    page_names_to_funcs = {
        "Software Engineer Basics": software_engineer_basics,
        "Basic ChatGPT": run_chatbot,
        "Python Agent": run_agent_py_programmer,
    }

    # # Use keys to define buttons
    # demo_name = st.sidebar.radio(
    #     "Choose a topic below:", key="visibility", options=page_names_to_funcs.keys()
    # )

    # Convert radio button to a dropdown (selectbox)
    demo_name = st.sidebar.selectbox(
        "Choose a topic below:", options=page_names_to_funcs.keys(), key="visibility"
    )

    # Display pages
    page_names_to_funcs[demo_name]()

elif st.session_state["authentication_status"] is False:
    st.error("Username/password is incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Please enter your username and password")

# Sidebar content
with st.sidebar:

    # Setup / Account Management
    with st.expander("Account🔒", expanded=False):

        # Creating password
        if st.session_state["authentication_status"]:
            try:
                if authenticator.reset_password(st.session_state["username"]):
                    st.success("Password modified successfully")
            except Exception as e:
                st.error(e)

        # Creating a new user registration
        try:
            (
                email_of_registered_user,
                username_of_registered_user,
                name_of_registered_user,
            ) = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success("User registered successfully")
        except Exception as e:
            st.error(e)

        # Create a forgot username
        try:
            username_of_forgotten_username, email_of_forgotten_username = (
                authenticator.forgot_username()
            )
            if username_of_forgotten_username:
                st.success("Username to be sent securely")
                # The developer should securely transfer the username to the user.
            elif username_of_forgotten_username == False:
                st.error("Email not found")
        except Exception as e:
            st.error(e)

        # Create a forgot password
        try:
            (
                username_of_forgotten_password,
                email_of_forgotten_password,
                new_random_password,
            ) = authenticator.forgot_password()
            if username_of_forgotten_password:
                st.success("New password to be sent securely")
                # The developer should securely transfer the new password to the user.
            elif username_of_forgotten_password == False:
                st.error("Username not found")
        except Exception as e:
            st.error(e)
