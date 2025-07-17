import streamlit as st
from datetime import  datetime
from components.ui.time_range_controller import (
    get_default_time_range,
)

def initialize_session_state():

    if "view_role" not in st.session_state:
        st.session_state.view_role = "admin"

    if "user_permissions" not in st.session_state:
        st.session_state.user_permissions = []

    if "user_variables_access" not in st.session_state:
        st.session_state.user_variables_access = []

    # ========= Project Controller ================
    if "create_pages" not in st.session_state:  
        st.session_state.create_pages = False
    
    # ======== Anedya ====================
    if "anedya_client" not in st.session_state:
        st.session_state.anedya_client = None

    if "nodeIds" not in st.session_state:
        st.session_state.nodesId = {}
        
    if "variables" not in st.session_state:
        st.session_state.variables= {}
    
    # ======== Firestore =================
    if "firestore_client" not in st.session_state:
        st.session_state.firestore_client = None
    

    # ======== HTTP ======================
    if "http_client" not in st.session_state:
        st.session_state.http_client = None


    # =========== Controllers ============
    if "door" not in st.session_state:
         st.session_state.door= "Open Door"

    if "light" not in st.session_state:
         st.session_state.light= "Turn Light On"

    if "fan" not in st.session_state:
         st.session_state.fan= "Turn Fan On"

    if "massage" not in st.session_state:
         st.session_state.massage= "Turn Massager On"

    #============== Door State ==================
    if "doorstate1" not in st.session_state:
        st.session_state.doorstate1 = 0

    if "doorstate2" not in st.session_state:
        st.session_state.doorstate2 = 0

    if "doorstate3" not in st.session_state:
        st.session_state.doorstate3 = 0

    if "doorstate4" not in st.session_state:
        st.session_state.doorstate4 = 0


    # ======== UI controller ======================
    if "show_charts" not in st.session_state:
        st.session_state.show_charts = ['Actual Temperature']

    # ======== Time Range controller ================
    default_time_range=[]
    if "from_date" not in st.session_state:
        default_time_range=get_default_time_range()
        st.session_state.from_date = default_time_range[2]

    if "to_date" not in st.session_state:
        st.session_state.to_date = default_time_range[0]

    if "from_time" not in st.session_state:
        st.session_state.from_time = default_time_range[3]

    if "to_time" not in st.session_state:
        st.session_state.to_time = default_time_range[1]

    if "from_input_time" not in st.session_state:
        current_date = datetime.now()
        epoach_time=int(current_date.timestamp())
        st.session_state.from_input_time = int(epoach_time - 86400)
    if "to_input_time" not in st.session_state:
        current_date = datetime.now()
        epoach_time=int(current_date.timestamp())
        st.session_state.to_input_time = epoach_time

    if "var_auto_update_time_range" not in st.session_state:
        st.session_state.var_auto_update_time_range = True




