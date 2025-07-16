"""uN Dashboard  by Anedya"""

import streamlit as st
import os
import json
import requests
from streamlit_autorefresh import st_autorefresh
from streamlit_db.session_storage import initialize_session_state
from cloud.firestore.firestore_client_handler import firebase_db_setup
from css.control_streamlit_cloud_features import hide_streamlit_style
from cloud.anedya_cloud import Anedya
from users_ui.admin.admin_dashboard import drawAdminDashboard
from users_ui.users.users_units_dashboard import drawUsersDashboard

DASHBOARD_NAME=st.secrets["DASHBOARD_NAME"]
st.set_page_config(page_title=DASHBOARD_NAME, layout="wide")

refresh_interval = 5000
st_autorefresh(interval=refresh_interval, limit=None, key="auto-refresh-handler", debounce=True)


# --------------- HELPER FUNCTIONS -----------------------
def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")


def main():
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # ---------------------- UI ---------------------------------------
    if st.session_state.LoggedIn is False:
        project_setup()
        drawLogin()
    else:
        if st.session_state.view_role == "admin":
            drawAdminDashboard()
        else:
            drawUsersDashboard()
            # pass


def project_setup():
    initialize_session_state() # Initialize Session State
    firebase_db_setup()  # Firebase client Setup
    st.session_state.http_client =requests.Session()
    # Manage Anedya Connection Credentials
    API_KEY=st.secrets["API_KEY"]
    anedya= Anedya()
    anedya_client = anedya.new_client(API_KEY)
    st.session_state.anedya_client = anedya_client

    NODES_ID = os.getenv("NODES_ID")
    NODES_ID_JSON = json.loads(NODES_ID)
    st.session_state.nodesId=NODES_ID_JSON
    VARIABLES = os.getenv("VARIABLES")
    VARIABLES_JSON = json.loads(VARIABLES)
    st.session_state.variables=VARIABLES_JSON


def drawLogin():
    current_dir=os.getcwd()
    NODES_NAME=st.session_state.nodesId["identifier"]
    pages = {
        f"{NODES_NAME}s": [
            st.Page(f"{current_dir}/nodes/node.py", title="Node"),
        ]
    }
    st.navigation(pages,position="hidden")

    cols = st.columns([1, 1.2, 1], gap="small")
    with cols[0]:
        pass
    with cols[1]:
            st.title("Dashboard Login", anchor=False)
            username_inp = st.text_input("Email").strip()
            password_inp = st.text_input("Password", type="password").strip()
            submit_button = st.button(label="Submit")
            if submit_button:
                check_credentials(username_inp, password_inp)
                print()
            

def check_credentials(username,password):
    if username =="admin@gmail.com":
        user_details = st.session_state.firestore_client.collection("tanUndefine").document(username).get().to_dict()
        if user_details is None:
          email="admin@gmail.com"
          name="Super Admin"
          password="admin"
          permissions=["ALL"]
          st.session_state.firestore_client.collection("tanUndefine").document(email).set({"name":name,"role":"admin","email":email,"password":password,"permissions":permissions,"variables_access":['ALL']},merge=True)

    user_details = st.session_state.firestore_client.collection("tanUndefine").document(username).get().to_dict()
    if user_details is None:
        st.error("Invalid Credential!")
        st.stop()
    if password != user_details["password"]:
        st.error("Incorrect Password!")
        st.stop()

    if user_details["role"] == "admin":
        st.session_state.view_role = "admin"
        st.session_state.LoggedIn = True
        st.rerun()
    elif user_details["role"] == "user":
        st.session_state.view_role = "user"
        st.session_state.user_permissions = user_details["permissions"]
        st.session_state.user_variables_access = user_details["variables_access"]
        st.session_state.LoggedIn = True
        st.rerun()

if __name__ == "__main__":
    main()
